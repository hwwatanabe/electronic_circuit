import numpy as np
#import matplotlib.pyplot as plt

#素子
E1=5.0
R2=2.0
R3=2.0
R4=4.0

#既約接続行列
Ar = np.array([[1,1,0,0],
              [0,-1,1,1]])

#インピーダンス行列
Z = np.array([[0,0,0,0],
             [0,R2,0,0],
             [0,0,R3,0],
             [0,0,0,R4]])

#ゼロ行列
Y = np.array([[0,0],
             [0,0]])

#電圧源ベクトル
EJ = np.array([E1,0,0,0,0,0])

A1 = np.c_[Ar.T, -Z]
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
