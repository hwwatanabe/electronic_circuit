#以下の２行はファイルの保存で必要
import matplotlib
#matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from sympy import *

from Waves import SquareWave

#ヘビサイド関数
def HeavisideFunction(t):
    return 0.5 * (np.sign(np.round(t,10)) + 1)

#解析解
def RCv(t, R, C):
    vc=E1*(1-np.exp(-t/(R*C)))*HeavisideFunction(t)
    return vc

#素子
R1=1.0
C2=1.0
E=3.0

#解析的をグラフ化する
dt1=0.01
t=np.arange(-1, 10, dt1)
E1=E*HeavisideFunction(t) #電源
v=RCv(t, R1, C2) #v(t)
#電圧プロット
plt.plot(t, E1, color="blue", linewidth=1.5, linestyle="--", label="$E$")
plt.plot(t, v, color="orange", linewidth=5.5, linestyle="-", label="Analytical")


#シミュレーションのパラメタ
E0 = symbols("E0", real=True)   #電圧源
dt=0.1  #シミュレーションステップ

#既約接続行列（電流源以外）
A = Matrix([[1,1,0],
            [0,-1,1]])
lenArow = A.rows
lenAcol = A.cols
print('Length of A col=', lenAcol)
print('Length of A row=', lenArow)

#電流源の既約接続行列
AJ = Matrix([0, 0])

#電流源ベクトル
J = Matrix([0])

#電圧源ベクトル
Ev = Matrix([E0,0,0])

#電圧源ベクトル
EJ = Matrix.vstack(Ev, -AJ*J)
print('----------------------------')
print('EJ=', simplify(EJ))

#インピーダンスを表す行列
Z = Matrix([[0,0,0],
            [0,R1,0],
            [0,0,dt/(2.0*C2)]])

#イプシロン行列
EPSILON = eye(lenAcol)
EPSILON[2,2]=-1.0
print('----------------------------')
print('varEpsilon=', simplify(EPSILON))

#デルタ行列
DELTA = eye(lenAcol)
print('----------------------------')
print('delta=', simplify(DELTA))

#ゼロ行列
Y = zeros(lenArow, lenArow)
Y2 = zeros(lenArow, lenAcol) #for CP matrix

#左辺側行列
print('****************************')
print('      left side matrix      ')
print('****************************')
#行列の接続
A1 = Matrix.hstack(A.T, -Z)
A2 = Matrix.hstack(Y, A)
C = simplify(Matrix.vstack(A1, A2))
print('----------------------------')
print('C=', C)

#右辺側行列
print('')
print('****************************')
print('     right side matrix      ')
print('****************************')
#行列の接続
CP1 = Matrix.hstack(EPSILON*A.T, -DELTA*Z)
CP2 = Matrix.hstack(Y, Y2)
CP = simplify(Matrix.vstack(CP1, CP2))
print('----------------------------')
print('CP=', CP)

#sympyからnumpyへの変換
invC=np.array(C.inv())
CPP=np.array(CP)
P=invC.dot(CPP)
PW=lambdify(E0, EJ, "numpy")

#UベクトルとIベクトルの作成
U0 = np.zeros((lenArow, 1))
U1 = np.zeros((lenArow, 1))
I0 = np.zeros((lenAcol, 1))
I1 = np.zeros((lenAcol, 1))
UI0 = np.r_[U0, I0]
UI1 = np.r_[U1, I1]

#シミュレーションパラメタと電源の設定
FinalTime=10.0
FinalInt = int(FinalTime/dt)
t2=np.arange(0.0, 10.0, dt)
SW=E*HeavisideFunction(t2)
x = np.arange(0, FinalTime, dt)
y = np.zeros(FinalInt)
PE0=0
PE1=0


for i in range(0, FinalInt):
    PE1=PW(SW[i])

    #Calculation
    UI1=-P.dot(UI0)+invC.dot(PE1+PE0)
    UI0=UI1
    PE0=PE1
    y[i]=UI1[1] #v(t)=u2(t)


#plot
#plt.xscale("log") #log scale
#plt.yscale("log")
plt.grid(which="both") #grid
plt.plot(x, y, color="blue", linewidth=1.5, linestyle="-", marker="o",
        markevery=1+int(0.5/dt), markersize=5.0, label="$v(t)$")
plt.xlabel("Time [sec]", fontsize=16)
plt.ylabel("v(t) [V]", fontsize=16)
plt.legend(loc='lower right')
plt.tick_params(labelsize=14)
#グラフの最大値・最小値
plt.xlim(-1, 10) #横軸の最大値・最小値
vmin=0.0
vmax=y.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

plt.show()
plt.savefig('graph.pdf')
