#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

from sympy import *
from sympy.plotting import plot

#文字の定義
v=Function('v')
t, v0 = symbols('t v0')
C0,C1,C2,C3=symbols('C:4') #微分方程式の解C0,C1,C2,C3を変数にする

C=1.0e-1
L=1.0
R=1.0
E0=1.0

print('-----------------------------------')
#微分方程式の設定
diffeq=L*C*v(t).diff(t,t)+R*C*v(t).diff(t)+v(t)-E0
#eq=Eq(L*C*v(t).diff(t,t)+R*C*v(t).diff(t)+v(t)-E0,0)
print('微分方程式：',diffeq,'= 0')

#微分方程式を解く
#ans1 = dsolve(diffeq, v(t), hint='best')
#print('微分方程式の一般解：', ans1.lhs, '=', simplify(ans1.rhs))

#微分方程式を解く
ans1 = dsolve(diffeq, v(t), hint='best')
ans1R=simplify(ans1.rhs)
ans1Rd=ans1R.diff(t)
print('微分方程式の一般解：', ans1R)

#初期条件の代入
ans2=ans1R.subs(t,0)
print('初期条件：v(0) =', ans2)
ans2d=ans1Rd.subs(t,0)
print('初期条件：vd(0) =', ans2d)
eq1a=Eq(ans2,0)
eq1b=Eq(ans2d,0)
ans3=solve([eq1a, eq1b], [C1, C2])
print(ans3)

ans4a=ans3[C1]
ans4b=ans3[C2]
ans1Rb=ans1R.subs([(C1, ans3[C1]),(C2, ans3[C2])])
print('微分方程式の解：v(t) =', ans1Rb)


#numpyへ変換
v1=lambdify(t, ans1Rb, "numpy")

#プロット用の配列
dt=0.01
t1=np.arange(0, 15, dt)
v=v1(t1)

#プロット
plt.plot(t1, v, color="blue", linewidth=2.5, linestyle="-", label=r"$v(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='upper right')
#グラフの最大値・最小値
plt.xlim(t1.min(), t1.max()) #横軸の最大値・最小値
vmin=-v.max()*0.0
vmax=v.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる
plt.show()
plt.savefig('graph.pdf')
