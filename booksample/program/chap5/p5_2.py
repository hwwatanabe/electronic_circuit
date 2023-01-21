#
# -*- coding: utf-8 -*-
#

#以下の２行はファイルの保存で必要
#import matplotlib
#matplotlib.use("Agg")

import numpy as np
#import matplotlib.pyplot as plt

J1=6.0
R2=2.0
R3=2.0
R4=4.0

#既約接続行列
Ar = np.array([[1,0,0],
              [-1,1,1]])

#インピーダンス行列
Z = np.array([[-R2,0,0],
             [0,-R3,0],
             [0,0,-R4]])

#ゼロ行列
Y = np.array([[0,0],
             [0,0]])

#電圧源ベクトル
EJ = np.array([0,0,0,6,0])

A1 = np.c_[Ar.T, Z]
A2 = np.c_[Y, Ar]
A = np.r_[A1, A2]

#節点ポテンシャルと素子電流を求める
x = np.linalg.solve(A, EJ)
print('-------------------------------')
print('(U I)=', x)

#素子電圧を求める
U = x[0:2]
V = Ar.T.dot(U)
print('-------------------------------')
print('V=', V)
