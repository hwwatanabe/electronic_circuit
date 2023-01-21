#以下の２行はファイルの保存で必要
import matplotlib
#matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from sympy import *

from Waves import SquareWave

#elements
R1=1.0
C2=1.0
V0=1.0

#simulation parameters
dt=0.01

#incidence matrix
A = Matrix([[1,1]])
lenArow = A.rows
lenAcol = A.cols
print('Length of A col=', lenAcol)
print('Length of A row=', lenArow)

#current source incident matrix
AJ = Matrix([0])

#current source vectors
J = Matrix([0])

#voltage source matrix
E = Matrix([0,0])

#電圧源ベクトル
EJ = Matrix.vstack(E, -AJ*J)
print('----------------------------')
print('EJ=', simplify(EJ))

#impedance matrix
Z = Matrix([[R1,0],
            [0,dt/(2.0*C2)]])

#varepsilon matrix
EPSILON = eye(lenAcol)
EPSILON[1,1]=-1.0
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

#initialize U and I vectors
U0 = np.zeros((lenArow, 1))
U1 = np.zeros((lenArow, 1))
I0 = np.zeros((lenAcol, 1))
I1 = np.zeros((lenAcol, 1))
UI0 = np.r_[U0, I0]
UI1 = np.r_[U1, I1]
UI0[0] = V0
UI0[1] = 1
#UI0[2] = -1
print('UI0=',UI1)

#simulation
FinalTime=10.0
FinalInt = int(FinalTime/dt)

x = np.arange(0, FinalTime, dt)
y = np.zeros(FinalInt)  #電圧
y2 = np.zeros(FinalInt) #電流

for i in range(0, FinalInt):
    #Calculation
    UI1=-P.dot(UI0)
    UI0=UI1
    y[i]=UI1[1] #電圧
    y2[i]=UI1[2]  #電流


#角周波数依存性のプロット
plt.figure(figsize=(8,9)) #サイズ設定
plt.subplot(2, 1, 1)
#plt.xscale("log") #対数表示
#plt.yscale("log")
plt.grid(which="both") #グリッドを入れる
plt.plot(x, y, color="blue", linewidth=2.5, linestyle="-", label=r"$v(t)$")
plt.xlabel("Time [sec]", fontsize=16)
plt.ylabel(r"$v(t)$ [V]", fontsize=16)
plt.legend(loc='upper right')
plt.ylim(-1.1, 1.1) #縦軸の最大値・最小値

plt.subplot(2, 1, 2)
#plt.xscale("log") #対数表示
#plt.yscale("log")
plt.grid(which="both") #グリッドを入れる
plt.plot(x, y2, color="red", linewidth=2.5, linestyle="-", label=r"$i(t)$")
plt.xlabel("Time [sec]", fontsize=16)
plt.ylabel(r"$i(t)$ [A]", fontsize=16)
plt.legend(loc='upper right')
plt.ylim(-1.1, 0.1) #縦軸の最大値・最小値

plt.tight_layout()  # タイトルの被りを防ぐ
plt.show()
plt.savefig('graph.pdf')
