#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

#素子の値
L=1.0
C=1.0e-1
#R=2.0*np.sqrt(L/C) #D=0の関係
R=1.0
E0=1.0
v00=0.0 #m=-1のとき
v0=0.0  #m=0のとき

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

def vc2(t): #D=0
    vc=(A12*np.exp(alpha*t)*np.cos(beta*t)+A22*np.exp(alpha*t)*np.sin(beta*t)+E0)*HeavisideFunction(t)
    return vc

#解析的
#プロット用の配列
dt=0.01
t=np.arange(-1, 15, dt)
#電源
E=E0*HeavisideFunction(t)

#v(t)
if D>0.0:
    v=vc0(t)
elif D==0.0:
    v=vc1(t)
else:
    v=vc2(t)

#グラフのサイズ
#plt.figure(figsize=(16, 5))

#電圧プロット
plt.plot(t, E, color="blue", linewidth=1.5, linestyle="--", label="$E$")
plt.plot(t, v, color="orange", linewidth=4.5, linestyle="-", label="Analytical")


#漸化式
dt2=[0.5, 0.01]  #配列を増やすことも可能
markerStyle=["o","s","v","^","P"]
for i in range(0, len(dt2)):
    #dt2=0.5
    t2=np.arange(0, 15, dt2[i])
    dt=dt2[i]
    vm=0*t2
    l=len(t2)
    K0=(L*dt*dt)/(L+R*dt)
    K1=(2*L*C+C*R*dt-dt*dt)/(dt*dt*L*C)
    K2=-1/(dt*dt)
    K3=E0/(L*C)
    #m=1のときは先に解いておく
    vm[1]=K0*(K1*v0+K2*v00+K3)
    for j in range(2, l):
        vm[j]=K0*(K1*vm[j-1]+K2*vm[j-2]+K3)
    labelText = r"$\Delta t$ ="+str(dt2[i])+"[s]"
    #プロット
    plt.plot(t2, vm, color='blue', linewidth=1.0, linestyle='-'
    , marker=markerStyle[i], markevery=int(0.5/dt), markersize=5.0, label=labelText)



plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='lower right')
plt.tick_params(labelsize=14)
#グラフの最大値・最小値
plt.xlim(-1, 15) #横軸の最大値・最小値
#vmin=v.min() * 1.1
#vmax=v.max() * 1.1
vmax=2.0
vmin=0.0
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
#plt.grid(which="both") #グリッドを入れる

plt.show()
plt.savefig('graph.pdf')
