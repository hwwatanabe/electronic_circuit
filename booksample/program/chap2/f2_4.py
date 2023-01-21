import matplotlib

#画像を保存するとき
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

from sympy import *
from sympy.plotting import plot

w, R = symbols('w R',real=True)
A = symbols('A')

#素子の値
C=1.0
L=1.0
E0=1.0
v0=0.0

#振幅（複素数）
A=E0/((1-w*w*L*C)+I*w*R*C) #sympyでは虚数はI

absA=Abs(A)
phaseA=arg(A)

print(phaseA)

#numpyの関数に変換
u1=lambdify((w, R), absA, "numpy")
p1=lambdify((w, R), phaseA, "numpy")

#角周波数の配列作成
w1=np.arange(0.1, 10.0, 0.01)

for i in range(0,3):
    rVal=10.0**(i-2.0) #抵抗の値

    #グラフの配列作成
    u2=u1(w1, rVal)
    p2=p1(w1, rVal)

    #変換
    #u3=np.log10(u2/E0)*20.0 #デシベルに変換
    u3=u2
    p3=p2*180/np.pi #degに変換

    #図のサイズ設定
    #plt.figure(figsize=(8,9))

    #プロットの設定
    rStr=str(rVal)+r"[$\Omega$]"
    if i==0:
        lStyl="-"
    elif i==1:
        lStyl="--"
    elif i==2:
        lStyl=":"

    #角周波数依存性のプロット
    plt.subplot(2, 1, 1)
    plt.xscale("log") #対数表示
    plt.yscale("log")
    plt.grid(which="major") #グリッドを入れる
    plt.plot(w1, u3, color="blue", linewidth=2, linestyle=lStyl, label=rStr)
    plt.xlabel("Angular Frequency [rad/s]", fontsize=14)
    plt.ylabel("Amplitude [V]", fontsize=14)
    plt.legend(loc='upper right', fontsize=10)

    plt.subplot(2, 1, 2)
    plt.xscale("log") #対数表示
    #plt.yscale("log")
    plt.grid(which="both") #グリッドを入れる
    plt.plot(w1, p3, color="red", linewidth=2, linestyle=lStyl, label=rStr)
    plt.xlabel("Angular Frequency [rad/s]", fontsize=14)
    plt.ylabel("Phase [deg]", fontsize=14)
    plt.legend(loc='upper right', fontsize=10)

#プロット間の縦の調整
plt.subplots_adjust(hspace = 0.3)

#画像の保存
plt.show()
plt.savefig('graph.pdf')
