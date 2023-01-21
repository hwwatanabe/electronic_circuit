'''

'''

import numpy as np
from sympy import *

from symOneDLine import symOneDLine
from boundaryClass import Boundary
from Waves import SquareWave


class oneDCircuit(symOneDLine):
    def __init__(self, lstLine, lstSource, lstLoad):
        # 伝送線路
        self.lineLength = lstLine[0]
        self.N = lstLine[1]
        self.mtlR = lstLine[2]
        self.lineNumber = lstLine[3]
        self.Z0 = lstLine[4]
        self.TD = lstLine[5]

        #ソース側
        self.A = lstSource[0]
        self.AJ = lstSource[1]
        self.J = lstSource[2]
        self.E = lstSource[3]
        self.ZL = lstSource[4]
        self.DLT = lstSource[5]
        self.EPSLN = lstSource[6]

        #負荷側
        self.AL = lstLoad[0]
        self.AJL = lstLoad[1]
        self.JL = lstLoad[2]
        self.EL = lstLoad[3]
        self.ZLL = lstLoad[4]
        self.DLTL = lstLoad[5]
        self.EPSLNL = lstLoad[6]


        #########################
        #     伝送線路の初期化    #
        #########################
        ln=symOneDLine(self.lineNumber,
                        self.lineLength,
                        self.mtlR,
                        self.N,
                        self.Z0,
                        self.TD
                        )

        # 伝送線路計算用行列
        self.txP = np.array(ln.Pmatrix) / ln.velocity
        self.invLRp = np.array(ln.invLRpM) / ln.dx
        self.invLRpLRm = np.array(ln.invLRpLRmM)
        self.dx = ln.dx
        self.lineLength = ln.lineLength

        #伝送線路ベクトルの初期化 (sympy => numpy)
        self.Ud0=np.array(ln.getUvec())
        self.Ud1=np.array(ln.getUvec())
        self.Id0=np.array(ln.getIvec())
        self.Id1=np.array(ln.getIvec())

        #########################
        #     ソース側の初期化    #
        #########################
        # source boundary
        src=Boundary(self.A,self.AJ,self.J,self.E,
                     self.ZL,self.DLT,self.EPSLN,ln.Zmatrix)

        #キャパシタとインダクタの設定
        #src.EPSILON[3,3]=-1.0
        #src.DELTA[1,1]=-1.0

        src.CMatrix() #C行列作成
        src.CPMatrix() #CP行列作成
        src.sympy2numpy2()  #伝送線路はsympy2numpy2()を使う
        # ソース側境界で用いる行列とベクトルの設定
        self.srcInvC = src.invC #C行列
        self.srcP = src.P #P=invC*CP
        self.srcEJ = src.EJ #電源ベクトル
        self.srcUI0 = src.initUI()
        self.srcUI1 = src.initUI()

        # 電源のsympy => numpyへの変換
        # This part must be changed according to the circuit.
        self.E0 = symbols("E0", real=True)
        self.PW=lambdify(self.E0, src.EJ, "numpy")



        #########################
        #      負荷側の初期化     #
        #########################
        # load boundary
        ld=Boundary(self.AL,self.AJL,self.JL,self.EL,
                    self.ZLL,self.DLTL,self.EPSLNL,ln.Zmatrix)

        ld.CMatrix()
        ld.CPMatrix()
        ld.sympy2numpy2()  #伝送線路はsympy2numpy2()を使う
        # 負荷側境界で用いる行列とベクトルの設定
        self.ldInvC = ld.invC
        self.ldP = ld.P
        self.ldEJ = ld.EJ
        self.ldUI0 = ld.initUI()
        self.ldUI1 = ld.initUI()

        # calculation conditions
        self.FinalTime = 1.0e-6
        self.FinalInt = int(self.FinalTime/ln.dt)
        self.PeriodTime=4.0e-9
        self.PeriodInt=int(self.PeriodTime/ln.dt)
        self.SW=SquareWave(1.0, self.PeriodTime/2.0, self.PeriodTime, ln.dt)   #パルス幅を決める

        #電源ベクトルの初期化
        self.PW1=self.PW(0.0)  #This needs to be arranged depending on the Power Supplies.
        self.PW0=self.PW(0.0)

        # for calculation
        self.src_num0 = src.lenArow + src.lenAcol - self.lineNumber
        self.src_num1 = src.lenArow + src.lenAcol
        self.ld_num0 = ld.lenArow + ld.lenAcol - self.lineNumber
        self.ld_num1 = ld.lenArow + ld.lenAcol

        self.i = 0

#    def startCalc(self):
#        for i in range(self.FinalInt):
#            self.calcLines(i)
#            print(i)

    def calcLines(self, i):

        # source boundary
        # power supply
        if (i<self.PeriodInt):
            self.E1=self.SW[i]
        else:
            self.E1=0
        self.PW1=self.PW(self.E1)   # one pulse
        #PW1=PW(SW[np.mod(i, PeriodInt)])   # repeat pulses
        #
        self.srcUI0[self.src_num0:self.src_num1,0] = self.srcUI0[self.src_num0:self.src_num1,0] - 2.0*self.Id0[:,1]
        self.srcUI1 = -self.srcP.dot(self.srcUI0)+self.srcInvC.dot(self.PW1+self.PW0)

        # load Boudanry
        self.ldUI0[self.ld_num0:self.ld_num1,0] = self.ldUI0[self.ld_num0:self.ld_num1,0] - 2.0*self.Id0[:,self.N]
        self.ldUI1 = -self.ldP.dot(self.ldUI0)

        # input values @ boundaries
        self.Ud1[:,0] = self.srcUI1[0:self.lineNumber,0]
        self.Id1[:,0] = self.srcUI1[self.src_num0:self.src_num1,0]
        self.Ud1[:,self.N] = self.ldUI1[0:self.lineNumber,0]
        self.Id1[:,self.N+1] = self.ldUI1[self.ld_num0:self.ld_num1,0]
        #self.baka=np.length(self.txP)
        #print('self.Ud1[:,1:self.N] =',self.baka)

        # calculation of lines
        self.Ud1[:,1:self.N]=-self.txP.dot(self.Id0[:,2:self.N+1]-self.Id0[:,1:self.N])+self.Ud0[:,1:self.N]
        self.Id1[:,1:self.N+1]=-self.invLRp.dot(self.Ud1[:,1:self.N+1]-self.Ud1[:,0:self.N])+self.invLRpLRm.dot(self.Id0[:,1:self.N+1])

        # k+1 => k
        self.srcUI0 = self.srcUI1
        self.ldUI0 = self.ldUI1
        self.Ud0 = self.Ud1
        self.Id0 = self.Id1
        self.PW0 = self.PW1
