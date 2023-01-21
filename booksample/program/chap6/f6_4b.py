#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

#素子の値
w=1.0
R=1.0
C=1.0
E0=1.0
v0=0.0

#ヘビサイド関数
def HeavisideFunction(t):
    return 0.5 * (np.sign(np.round(t,10)) + 1)

#v(t)
def RCv(t):
    vc=E0*(1-np.exp(-t/(R*C)))*HeavisideFunction(t)
    return vc



#解析的
dt=0.01
t=np.arange(-1, 10, dt)
E=E0*HeavisideFunction(t) #電源
v=RCv(t) #v(t)
#解析解のプロット
#plt.plot(t, v, color="red", linewidth=1.5, linestyle="-", label="Analytical")
#電圧プロット
plt.plot(t, E, color="blue", linewidth=1.5, linestyle="--", label="$E$")
plt.plot(t, v, color="orange", linewidth=4.5, linestyle="-", label="Analytical")



#漸化式
dt2=[1.0, 0.5, 0.1, 0.01]
markerStyle=["o","s","+","v","^"]
for i in range(0, len(dt2)):
    #dt2=0.5
    t2=np.arange(0, 10, dt2[i])
    dt=dt2[i]
    vm=0*t2 #初期化
    l=len(t2)
    for j in range(1, l):
        vm[j]=((R*C)/(dt+R*C))*vm[j-1]+(E0*dt)/(R*C+dt)
    labelText = r"$\Delta t$ ="+str(dt2[i])+"[s]"
    #プロット
    plt.plot(t2, vm, color='blue', linewidth=1.0, linestyle='-'
    , marker=markerStyle[i], markevery=1+int(0.5/dt), markersize=5.0, label=labelText)



#グラフのサイズ
#plt.figure(figsize=(10, 5))


#プロットの調整
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='lower right')
plt.tick_params(labelsize=14)
#グラフの最大値・最小値
plt.xlim(-1, 10) #横軸の最大値・最小値
vmin=0.0
vmax=v.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

plt.show()
plt.savefig('graph.pdf')
