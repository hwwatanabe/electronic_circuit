#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

from sympy import *
from sympy.plotting import plot

#文字の定義
v=Function('v')
diffeq=Function('diffeq')
t=Symbol('t')

#素子
E0=1.0
R1=1.0
R2=1.0
R3=1.0
C=1.0  #C4

#任意変数
C0,C1,C2,C3=symbols('C:4') #微分方程式の解C0,C1,C2,C3を変数にする

print('-----------------------------------')

#微分方程式の設定
a1=R1*R2+R2*R3+R3*R1
a0=(R1+R3)/C
diffeq=a1*v(t).diff(t)+a0*v(t)-E0/C
print('微分方程式：',diffeq,'= 0')

#微分方程式を解く
ans1 = dsolve(diffeq, v(t), hint='best')
ans1R=simplify(ans1.rhs)
print('微分方程式の一般解：', ans1.lhs, '=', simplify(ans1.rhs))

#初期条件の代入
v0=(R1+R3)*E0/a1
ans2=ans1R.subs(t,0)
print('初期条件：v(0) =', ans2)
eq1=Eq(ans2-v0,0)
ans3=solve(eq1, C1)
#print(ans3[0])
ans4=ans1R.subs(C1,ans3[0])
print('微分方程式の解：', ans1.lhs, '=', simplify(ans4))

#numpyへ変換
v1=lambdify(t, ans4, "numpy")

#プロット用の配列
dt=0.1
t1=np.arange(0, 10, dt)
v2=v1(t1)

#プロット
plt.plot(t1, v2, color="blue", linewidth=2.5, linestyle="-", label=r"$i(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Current [A]", fontsize=16)
plt.legend(loc='upper right')
#グラフの最大値・最小値
plt.xlim(t1.min(), t1.max()) #横軸の最大値・最小値
vmin=-v2.max()*0.0
vmax=v2.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる
plt.show()
plt.savefig('graph.pdf')
