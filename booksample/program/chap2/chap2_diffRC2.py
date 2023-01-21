from sympy import *

#文字の定義
v=Function('v')
diffeq=Function('diffeq')
t=Symbol('t')
R=Symbol('R')
C=Symbol('C')
E0=Symbol('E0')
v0=Symbol('v0')
C0,C1,C2,C3=symbols('C:4') #微分方程式の解C0,C1,C2,C3を変数にする

print('-----------------------------------')

#微分方程式の設定
diffeq=R*C*v(t).diff(t)+v(t)-E0
print('微分方程式：',diffeq,'= 0')

#微分方程式を解く
ans1 = dsolve(diffeq, v(t), hint='best')
ans1R=simplify(ans1.rhs)
print('微分方程式の一般解：', ans1.lhs, '=', simplify(ans1.rhs))

#初期条件の代入
ans2=ans1R.subs(t,0)
print('初期条件：v(0) =', ans2)
eq1=Eq(ans2,0)
ans3=solve(eq1, C1)
#print(ans3[0])
ans4=ans1R.subs(C1,ans3[0])
print('微分方程式の解：', ans1.lhs, '=', simplify(ans4))
