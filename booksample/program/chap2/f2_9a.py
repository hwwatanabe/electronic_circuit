#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

#素子の値
L=1.0
C=1.0e-1
R=20.0 #D>0
#R=2.0*np.sqrt(L/C) #D=0の関係
#R=1.0  #D<0
E0=1.0
v0=0.0

#判別式
D=np.round(np.power(C*R,2)-4.0*L*C,10) #小数点第10位を四捨五入
print('D=',D)

#定数の計算
if D>0:
    lambda1=(-C*R+np.sqrt(D))/(2*L*C)
    lambda2=(-C*R-np.sqrt(D))/(2*L*C)
    A10=lambda2*E0/(lambda1-lambda2)
    A20=-lambda1*E0/(lambda1-lambda2)
if D==0:
    lambda1= -R/(2.0*L)
    lambda2= -R/(2.0*L)
    A11=-E0
    A21=lambda1*E0
else: #D<0
    alpha=-R/(2*L)
    beta=np.sqrt(-D)/(2*L*C)
    A12=-E0
    A22=alpha*E0/beta



#ヘビサイド関数
def HeavisideFunction(t):
    return 0.5 * (np.sign(np.round(t,10)) + 1)

#v(t)
def vc0(t): #D>0
    #vc=1*t
    #vc=a21*np.exp(lambda2*t)+E0
    vc=(A10*np.exp(lambda1*t)+A20*np.exp(lambda2*t)+E0)*HeavisideFunction(t)
    return vc

def vc1(t): #D=0
    vc=(A11*np.exp(lambda1*t)+A21*t*np.exp(lambda1*t)+E0)*HeavisideFunction(t)
    return vc

def vc2(t): #D<0
    vc=(A12*np.exp(alpha*t)*np.cos(beta*t)+A22*np.exp(alpha*t)*np.sin(beta*t)+E0)*HeavisideFunction(t)
    return vc

#プロット用の配列
dt=0.01
t=np.arange(-1, 10, dt)

#電源
E=E0*HeavisideFunction(t)

#v(t)
if D>0.0:
    v=vc0(t)
elif D==0.0:
    v=vc1(t)
else:
    v=vc2(t)

print(v)

#グラフのサイズ
#plt.figure(figsize=(16, 5))

#電圧プロット
plt.plot(t, E, color="blue", linewidth=2.5, linestyle="--", label=r"$E$")
plt.plot(t, v, color="red", linewidth=2.5, linestyle="-", label=r"$v(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='lower right')
#グラフの最大値・最小値
plt.xlim(-1, 10) #横軸の最大値・最小値
#vmin=v.min() * 1.1
#vmax=v.max() * 1.1
vmax=1.6
vmin=0.0
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

plt.show()
plt.savefig('graph.pdf')
