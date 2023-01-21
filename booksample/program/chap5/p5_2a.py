#
# -*- coding: utf-8 -*-
#

from sympy import *
J1, R2, R3, R4 = symbols("J1 R2 R3 R4")

#既約接続行列
Ar = Matrix([[1,0,0],
             [-1,1,1]])

#インピーダンス行列
Z = Matrix([[-R2,0,0],
            [0,-R3,0],
            [0,0,-R4]])

#ゼロ行列
Y = Matrix([[0,0],
            [0,0]])

#電源ベクトル
EJ = Matrix([0,0,0,J1,0])

#方程式
A1 = Matrix.hstack(Ar.T, Z)
A2 = Matrix.hstack(Y, Ar)
A = Matrix.vstack(A1, A2)

#節点ポテンシャルと素子電流を求める
x = simplify(A.inv() * EJ)
print('-------------------------------')
print('(U I)=', x)

#素子電圧を求める
U = Matrix(x[0:2])
V = simplify(Matrix(Ar.T.dot(U)))
print('-------------------------------')
print('V=', V)
