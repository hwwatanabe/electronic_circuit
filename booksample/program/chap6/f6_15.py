#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from sympy import *

#ヘビサイド関数
def HeavisideFunction(t):
    return 0.5 * (np.sign(np.round(t,10)) + 1)

#フーリエ級数で矩形波を出力
#a:1の時間、b:ゼロの時間
def SquareWave(t,a,b):
    n=10000 #調整必要、通常はこれくらい？
    sw=a/(a+b)
    for i in range(n):
        sw += (2.0/(i+1)/np.pi)*np.sin((i+1)*a*np.pi/(a+b))*np.cos((t-a/2.0)*2.0*np.pi*(i+1)/(a+b))
    return sw



#素子
R1=1.0
C2=1.0
E0 = symbols("E0", real=True)

#シミュレーションパラメタ
dt=0.01  #ステップ
startTime=-1.0
finalTime=10.0  #終了時刻
t1=2.0
t2=1.0
t=np.arange(startTime, finalTime, dt)

#電圧源
#説明：ステップ関数のときは
#少し傾きをもたせないと
#うまくシミュレーションできないため
#その処理をしている
e1=np.round(HeavisideFunction(t)*SquareWave(t,t1,t2))
de1=np.diff(e1)
for i in range(0, de1.size):
    if not de1[i]==0:
        e1[i+1]=1/2
e1=e1*1.0  #ステップの高さ設定

#incidence matrix
A = Matrix([[1,1,1]])
lenArow = A.rows
lenAcol = A.cols
print('Length of A col=', lenAcol)
print('Length of A row=', lenArow)

#current source incident matrix
AJ = Matrix([0])

#current source vectors
J = Matrix([0])

#voltage source matrix
E = Matrix([E0,0,0])

#電圧源ベクトル
EJ = Matrix.vstack(E, -AJ*J)
print('----------------------------')
print('EJ=', simplify(EJ))

#impedance matrix
Z = Matrix([[0,0,0],
            [0,R1,0],
            [0,0,dt/(2.0*C2)]])

#varepsilon matrix
EPSILON = eye(lenAcol)
EPSILON[2,2]=-1.0
print('----------------------------')
print('varEpsilon=', simplify(EPSILON))

#delta matrix
DELTA = eye(lenAcol)
print('----------------------------')
print('delta=', simplify(DELTA))

#zero matrix
Y = zeros(lenArow, lenArow)
Y2 = zeros(lenArow, lenAcol) #for CP matrix

#calculation left side matrix
print('****************************')
print('      left side matrix      ')
print('****************************')
#combine matrices
A1 = Matrix.hstack(A.T, -Z)
A2 = Matrix.hstack(Y, A)
C = simplify(Matrix.vstack(A1, A2))
print('----------------------------')
print('C=', C)

print('')
print('****************************')
print('     right side matrix      ')
print('****************************')
#combine matrices
CP1 = Matrix.hstack(EPSILON*A.T, -DELTA*Z)
CP2 = Matrix.hstack(Y, Y2)
CP = simplify(Matrix.vstack(CP1, CP2))
print('----------------------------')
print('CP=', CP)

#convert to sympy to numpy
invC=np.array(C.inv())
CPP=np.array(CP)
P=invC.dot(CPP)
PW=lambdify(E0, EJ, "numpy")

#initialize U and I vectors
U0 = np.zeros((lenArow, 1))
U1 = np.zeros((lenArow, 1))
I0 = np.zeros((lenAcol, 1))
I1 = np.zeros((lenAcol, 1))
UI0 = np.r_[U0, I0]
UI1 = np.r_[U1, I1]

#グラフ描画用配列
y = np.zeros(t.size)

PE0=PW(0.0)
PE1=PW(0.0)

for i in range(0, t.size):
    PE1=PW(e1[i])

    #Calculation
    UI1=-P.dot(UI0)+invC.dot(PE1+PE0)
    #print('P.dot(UI0)=',P.dot(UI0))
    #print('invC.dot(PE1+PE0)=',invC.dot(PE1+PE0))
    #print('UI1=',UI1)
    y[i]=UI1[3]
    #y[i]=(UI1[3]+UI0[3])/2.0
    UI0=UI1
    PE0=PE1



#plot
#plt.xscale("log") #log scale
#plt.yscale("log")
plt.grid(which="both") #grid
#plt.plot(t, e1, color="blue", linewidth=1.5, linestyle="--", label="e(t)")
plt.plot(t, y, color="blue", linewidth=1.5, linestyle="-", label=r"$i(t)$")
plt.xlabel("Time [sec]", fontsize=16)
plt.ylabel("Current [A]", fontsize=16)
plt.legend(loc='upper right')
plt.xlim(startTime, finalTime) #縦軸の最大値・最小値
plt.ylim(-120, 120) #縦軸の最大値・最小値
plt.show()
plt.savefig('graph.pdf')
print(e1)
