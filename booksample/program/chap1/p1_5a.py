from sympy import *

# calculation
t, C=symbols("t C", real=True)
v0=Heaviside(t) #ヘビサイド関数の電圧
i0=C*diff(v0,t) #キャパシタに流れる電流
print("v(t)=", v0)
print("i(t)=", i0)
