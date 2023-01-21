#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from sympy import *

#from Waves import SquareWave




#素子
#E, R, C, w = symbols('E R C w', real=True)
E=1.0
R=1.0
C=1.0
w=1.0
#V = Function('V')
#IC = Function('IC')
V, IC = symbols('V IC')

#解くべき方程式 =0とする
eq1=Eq(E-R*IC-V,0)
eq2=Eq(IC-I*w*C*V,0)


#方程式を解く
ans1=solve([eq1, eq2], [V, IC])

print('-----------------------------------')
print('V =', ans1[V])
print('絶対値：|V| = ',Abs(ans1[V]) )
print('偏角：Arg(V) = ',arg(ans1[V]) )
