#以下の２行はファイルの保存で必要
import matplotlib
#matplotlib.use("Agg")

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
E0=1.0
L3=1.0
C4=1.0e-1
R2=20.0  #判別式 D>0
#R2=2.0*np.sqrt(L3/C4)  #判別式 D=0
#R2=1.0  #判別式 D<0


dt=0.1  #シミュレーションステップ
finalTime=60.0  #シミュレーション終了時間
t1=15.0
t2=15.0
t=np.arange(-1, finalTime, dt)

#電圧源　（ｔ＞０）
e1=HeavisideFunction(t)*SquareWave(t,t1,t2)


#シミュレーションのパラメタ
E1 = symbols("E1", real=True)   #電圧源

#既約接続行列（電流源以外）
A = Matrix([[1,1,0,0],
            [0,-1,1,0],
            [0,0,-1,1]])
lenArow = A.rows
lenAcol = A.cols
print('Length of A col=', lenAcol)
print('Length of A row=', lenArow)

#電流源の既約接続行列
AJ = Matrix([0,0,0])

#電流源ベクトル
J = Matrix([0])

#電圧源ベクトル
Ev = Matrix([E1,0,0,0])

#電圧源ベクトル
EJ = Matrix.vstack(Ev, -AJ*J)
print('----------------------------')
print('EJ=', simplify(EJ))

#インピーダンスを表す行列
Z = Matrix([[0,0,0,0],
            [0,R2,0,0],
            [0,0,(2.0*L3)/dt,0],
            [0,0,0,dt/(2.0*C4)]])

#イプシロン行列
EPSILON = eye(lenAcol)
EPSILON[3,3]=-1.0
print('----------------------------')
print('varEpsilon=', simplify(EPSILON))

#デルタ行列
DELTA = eye(lenAcol)
DELTA[2,2]=-1.0
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
PW=lambdify(E1, EJ, "numpy")

#UベクトルとIベクトルの作成
U0 = np.zeros((lenArow, 1))
U1 = np.zeros((lenArow, 1))
I0 = np.zeros((lenAcol, 1))
I1 = np.zeros((lenAcol, 1))
UI0 = np.r_[U0, I0]
UI1 = np.r_[U1, I1]

#グラフ描画用配列
y = np.zeros(t.size)

PE0=0
PE1=0

for i in range(t.size):
    PE1=PW(e1[i])
    #Calculation
    UI1=-P.dot(UI0)+invC.dot(PE1+PE0)
    UI0=UI1
    PE0=PE1
    y[i]=UI1[2] #v(t)=u2(t)


#plot
#plt.xscale("log") #log scale
#plt.yscale("log")
plt.grid(which="both") #grid

#電圧源プロット
plt.plot(t, e1, color="blue", linewidth=2.5, linestyle="--", label="$e_1(t)$")
#シミュレーション結果のプロット
#plt.plot(t, y, color="blue", linewidth=1.5, linestyle="-", marker="o",
#        markevery=1+int(1.0/dt), markersize=5.0, label="Simulation")
plt.plot(t, y, color="red", linewidth=2.5, linestyle="-", label="$v(t)$")

plt.xlabel("Time [sec]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='upper right')
plt.tick_params(labelsize=14)
#グラフの最大値・最小値
plt.xlim(0.0, finalTime) #横軸の最大値・最小値
vmin=-0.7
vmax= 1.7
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

plt.show()
plt.savefig('graph.pdf')
