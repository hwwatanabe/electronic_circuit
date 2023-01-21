
# -*- coding: utf-8 -*-
"""
Boundary class
"""

import numpy as np
from sympy import *


class Boundary:

    #コンストラクタ
    # A:接続行列（伝送線路含む）
    # AJ:電流源の接続行列
    # J:電流源ベクトル
    # E:電圧源ベクトル
    # ZL:集中定数側のインピーダンス
    # DLT:デルタ行列
    # EPSLN:イプシロン行列
    # ZC:伝送線路の特性インピーダンス
    def __init__(self, A, AJ, J, E, ZL, DLT, EPSLN, ZC):
        #接続行列
        self.A = A
        self.AJ = AJ
        self.J = J
        self.E = E
        self.ZL = ZL
        self.DLT=DLT
        self.EPSLN=EPSLN
        self.ZC = ZC

        #接続行列の行数・列数
        self.lenArow = self.A.rows
        self.lenAcol = self.A.cols
        print('----------------------------')
        print('Length of A col=', self.lenAcol)
        print('Length of A row=', self.lenArow)

        #インピーダンス行列の連結
        self.lenZL = self.ZL.rows
        self.lenZC = self.ZC.rows
        self.Z1 = zeros(self.lenZL, self.lenZC)
        self.Z2 = zeros(self.lenZC, self.lenZL)
        self.Z3 = Matrix.hstack(self.ZL, self.Z1)
        self.Z4 = Matrix.hstack(self.Z2, self.ZC)
        self.Z = Matrix.vstack(self.Z3, self.Z4)
        print('----------------------------')
        print('Z=', simplify(self.Z))

        #電圧源ベクトルの作成
        self.EJ = Matrix.vstack(self.E, -self.AJ*self.J)
        print('----------------------------')
        print('EJ=', simplify(self.EJ))

        #varepsilon matrix
        self.EPSILOND = -eye(self.lenZC)
        self.EPSILON1 = zeros(self.lenZL, self.lenZC)
        self.EPSILON2 = zeros(self.lenZC, self.lenZL)
        self.EPSILON3 = Matrix.hstack(self.EPSLN, self.EPSILON1)
        self.EPSILON4 = Matrix.hstack(self.EPSILON2, self.EPSILOND)
        self.EPSILON = Matrix.vstack(self.EPSILON3, self.EPSILON4)
        print('----------------------------')
        print('EPSILON=', simplify(self.EPSILON))


        #delta matrix
        self.DELTAD = eye(self.lenZC)
        self.DELTA1 = zeros(self.lenZL, self.lenZC)
        self.DELTA2 = zeros(self.lenZC, self.lenZL)
        self.DELTA3 = Matrix.hstack(self.DLT, self.DELTA1)
        self.DELTA4 = Matrix.hstack(self.DELTA2, self.DELTAD)
        self.DELTA = Matrix.vstack(self.DELTA3, self.DELTA4)
        print('----------------------------')
        print('DELTA=', simplify(self.DELTA))

        #print('----------------------------')
        #print('delta=', simplify(self.DELTA))

        #zero matrix
        self.Y = zeros(self.lenArow, self.lenArow)
        self.Y2 = zeros(self.lenArow, self.lenAcol) #for CP matrix

    def CMatrix(self):
        #calculation left side matrix
        self.A1 = Matrix.hstack(self.A.T, -self.Z)
        self.A2 = Matrix.hstack(self.Y, self.A)
        self.C = simplify(Matrix.vstack(self.A1, self.A2))
        print('----------------------------')
        print('****************************')
        print('      left side matrix      ')
        print('****************************')
        print('C=', self.C)
        return self.C

    def CPMatrix(self):
        #calculation right side matrix
        self.CP1 = Matrix.hstack(self.EPSILON*self.A.T, -self.DELTA*self.Z)
        self.CP2 = Matrix.hstack(self.Y, self.Y2)
        self.CP = simplify(Matrix.vstack(self.CP1, self.CP2))
        print('----------------------------')
        print('****************************')
        print('     right side matrix      ')
        print('****************************')
        print('CP=', self.CP)
        return self.CP

    def sympy2numpy(self):
        #convert to sympy to numpy
        self.invC=np.array(self.C.inv())

    def sympy2numpy2(self):
        #convert to sympy to numpy
        self.invC=np.array(self.C.inv())
        self.CPP=np.array(self.CP)
        self.P=self.invC.dot(self.CPP)

    def initUI(self):
        #initialize U and I vectors
        self.U0 = np.zeros((self.lenArow, 1))
        #self.U1 = np.zeros((self.lenArow, 1))
        self.I0 = np.zeros((self.lenAcol, 1))
        #self.I1 = np.zeros((self.lenAcol, 1))
        #self.UI0 = np.r_[self.U0, self.I0]
        #self.UI1 = np.r_[self.U1, self.I1]
        return np.r_[self.U0, self.I0]

# end of Circuit class
