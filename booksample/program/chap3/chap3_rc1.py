#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from sympy import *

#from Waves import SquareWave




#素子
E, R, C, w = symbols('E R C w', real=True)
V = Function('V')
IC = Function('IC')

#解くべき方程式 =0とする
eq1=Eq(E-R*IC(w)-V(w),0)
eq2=Eq(IC(w)-I*w*C*V(w),0)


#方程式を解く
ans1=solve([eq1, eq2], [V(w), IC(w)])

print('-----------------------------------')
print('V =', ans1[V(w)])
print('絶対値：|V| = ',Abs(ans1[V(w)]) )
print('偏角：Arg(V) = ',arg(ans1[V(w)]) )
