# -*- coding: utf-8 -*-
import matplotlib
from oneDCircuit import oneDCircuit
from symOneDLine import symOneDLine
from Waves import SquareWave #信号源
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



###############################
#          伝送線路
#
# mtl = [[aii_1, d1j_1, r_1],
#        [aii_2, d1j_2, r_2], .....]
# mtl: 伝送線路の情報
# aii: 伝送線の半径
# d1j: 伝送線の距離（１本目からの）
# r: 伝送線の単位長さあたりの抵抗 ohm/m
###############################
l=1.0   #長さ
er=3.0  #比誘電率
mr=1.0  #比透磁率
Nx=200  #分割数
mtl = Matrix([[0.001,0,0],
             [0.001,0.01,0],
             [0.001,0.005,0]])

#プロットのパラメタ
x=np.linspace(0, l, Nx+1) #0-lの間にNx+1の配列をつくる

lN = mtl.rows  #伝送線の本数

#伝送線のリスト
lstLn=[l,Nx,mtl,lN,er,mr]

#伝送線路の初期化用リスト
ln=symOneDLine(lN, l, mtl, Nx, er, mr)
dt=ln.dt
print('----------------------------')
print('dt=',dt)



###############################
#          ソース側
###############################
#素子
#RS=159.417
# RSを１本目と２本目の間の特性インピーダンスにあわせる
RS=ln.Zmatrix[0,0]+ln.Zmatrix[1,1]-(ln.Zmatrix[0,1]+ln.Zmatrix[1,0])
R23=1e6
R13=R23

#電源
E0 = symbols("E0", real=True)
#ここではsympyで定義して、
#あとでnumpyに変換している

#接続行列
A = Matrix([[0,1,0,1,1,0,0],
            [-1,0,1,0,0,1,0],
            [0,0,-1,-1,0,0,1],
            [1,-1,0,0,0,0,0]])
#電流源
AJ = Matrix([0,0,0,0])

#電流源ベクトル
J = Matrix([0])

#電圧源ベクトル
E = Matrix([E0,0,0,0,0,0,0])

#インピーダンス行列
ZL = Matrix([[0,0,0,0],
             [0,RS,0,0],
             [0,0,R23,0],
             [0,0,0,R13]])

#デルタ行列（集中＋分布）
DLT = Matrix([[1,0,0,0],
              [0,1,0,0],
              [0,0,1,0],
              [0,0,0,1]])

#イプシロン行列（集中＋分布）
EPSLN = Matrix([[1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,0,1]])

#ソース側の初期化用リスト
lstSrc=[A,AJ,J,E,ZL,DLT,EPSLN]

###############################
#           負荷側
###############################
#素子
RL=RS

#接続行列
AL = Matrix([[1,-1,0,0],
             [-1,0,-1,0],
             [0,0,0,-1]])
#電流源
AJL = Matrix([0,0,0,0])

#電流源ベクトル
JL = Matrix([0])

#電圧源ベクトル
EL = Matrix([0,0,0])

#インピーダンス行列
ZLL = Matrix([RL])

#デルタ行列（集中＋分布）
DLTL = Matrix([1])

#イプシロン行列（集中）
EPSLNL = Matrix([1])

#負荷側の初期化用リスト
lstLd=[AL,AJL,JL,EL,ZLL,DLTL,EPSLNL]


###############################
#     １次元伝送線回路の初期化
###############################
cr = oneDCircuit(lstLn, lstSrc, lstLd)


###############################
#     １次元伝送線計算準備
###############################
'''
#各行列・ベクトル設定
srcUI0=cr.srcUI0
srcUI1=cr.srcUI1
Id0=cr.Id0
srcP=cr.srcP
srcInvC=cr.srcInvC
src_num0=cr.src_num0
src_num1=cr.src_num1
#
ldUI0=cr.ldUI0
ldUI1=cr.ldUI1
Id0=cr.Id0
ldP=cr.ldP
ldInvC=cr.ldInvC
ld_num0=cr.ld_num0
ld_num1=cr.ld_num1
#
Ud0=cr.Ud0
Id0=cr.Id0
Ud1=cr.Ud1
Id1=cr.Id1
txP=cr.txP
invLRp=cr.invLRp
invLRpLRm=cr.invLRpLRm
'''

#ソース側電源
PeriodTime=1.0e-9
PeriodInt=int(PeriodTime/dt)
SW=SquareWave(1.0, PeriodTime/2.0, PeriodTime, dt)   #パルス幅を決める
# 電源ベクトルのsympy => numpyへの変換
#self.E0 = symbols("E0", real=True)
PW=lambdify(cr.E0, cr.srcEJ, "numpy")
#電源ベクトルの初期化
PW1=PW(0.0)
PW0=PW(0.0)


# 伝送線路計算
def calcLines(i, cr):
    #global cr, PW1, PW0, SW, PeriodInt
    global PW1, PW0, SW, PeriodInt
    # 電源
    if (i<PeriodInt):
        E1=SW[i]
    else:
        E1=0
    PW1=PW(E1)   # １回のパルス
    #PW1=PW(SW[np.mod(i, PeriodInt)])   # 繰り返しパルス

    #ソース側境界の計算
    cr.srcUI0[cr.src_num0:cr.src_num1,0] = cr.srcUI0[cr.src_num0:cr.src_num1,0] - 2.0*cr.Id0[:,1]
    cr.srcUI1 = -cr.srcP.dot(cr.srcUI0)+cr.srcInvC.dot(PW1+PW0)

    #負荷側境界の計算
    cr.ldUI0[cr.ld_num0:cr.ld_num1,0] = cr.ldUI0[cr.ld_num0:cr.ld_num1,0] - 2.0*cr.Id0[:,cr.N]
    cr.ldUI1 = -cr.ldP.dot(cr.ldUI0)

    # 境界での計算結果を伝送線路の境界に代入
    cr.Ud1[:,0] = cr.srcUI1[0:cr.lineNumber,0]
    cr.Id1[:,0] = cr.srcUI1[cr.src_num0:cr.src_num1,0]
    cr.Ud1[:,cr.N] = cr.ldUI1[0:cr.lineNumber,0]
    cr.Id1[:,cr.N+1] = cr.ldUI1[cr.ld_num0:cr.ld_num1,0]

    # 伝送線路の計算
    cr.Ud1[:,1:cr.N]=-cr.txP.dot(cr.Id0[:,2:cr.N+1]-cr.Id0[:,1:cr.N])+cr.Ud0[:,1:cr.N]
    cr.Id1[:,1:cr.N+1]=-cr.invLRp.dot(cr.Ud1[:,1:cr.N+1]-cr.Ud1[:,0:cr.N])+cr.invLRpLRm.dot(cr.Id0[:,1:cr.N+1])

    # 結果を１つ前の変数に代入
    cr.srcUI0 = cr.srcUI1
    cr.ldUI0 = cr.ldUI1
    cr.Ud0 = cr.Ud1
    cr.Id0 = cr.Id1
    PW0 = PW1

    return [np.float_(cr.Ud1[0]-cr.Ud1[1]), np.float_(cr.Ud1[1]-cr.Ud1[2])]
    #return np.float_(cr.Ud1[0]-cr.Ud1[1])



##########################
#逐次計算しながらアニメーションで表示する
##########################
fig = plt.figure()

i=0
def plot(data):
    global i

    data = calcLines(i,cr)    # 計算
    i += 1

    #グラフの描画
    plt.subplot(2,1,1)
    plt.cla()   # 現在描写されているグラフを消去
    plt.plot(x, data[0], color="red",
        linewidth=1.5, linestyle="-", label="$U_1(x,t)-U_2(x,t)$")    # グラフを生成
    plt.xlabel("Position x [m]", fontsize=16)
    plt.ylabel("Voltage [V]", fontsize=16)
    plt.legend(loc='lower right')
    plt.tick_params(labelsize=14)
    plt.xlim(0.0, l)            #横軸の最大値・最小値
    plt.ylim(-1.5, 1.0)         #縦軸の最大値・最小値
    plt.grid(which="both")      #グリッドを入れる
    jikan='t=' + '%.2e'%(dt*i) + '[s]'
    plt.text(0.01,0.75,jikan, ha = 'left', va = 'center', fontsize=14)

    plt.subplot(2,1,2)
    plt.cla()   # 現在描写されているグラフを消去
    im2 = plt.plot(x, data[1], color="blue",
        linewidth=1.5, linestyle="-", label="$U_2(x,t)-U_3(x,t)$")    # グラフを生成
    plt.xlabel("Position x [m]", fontsize=16)
    plt.ylabel("Voltage [V]", fontsize=16)
    plt.legend(loc='lower right')
    plt.tick_params(labelsize=14)
    plt.xlim(0.0, l)            #横軸の最大値・最小値
    plt.ylim(-1, 1)         #縦軸の最大値・最小値
    plt.ticklabel_format(style='sci',axis='y',scilimits=(0,0))  #縦軸を指数で表記
    plt.grid(which="both")      #グリッドを入れる
    plt.text(0.01,0.15,jikan, ha = 'left', va = 'center', fontsize=14)

    plt.tight_layout()  # タイトルの被りを防ぐ


ani = animation.FuncAnimation(fig, plot, interval=10)
plt.show()
