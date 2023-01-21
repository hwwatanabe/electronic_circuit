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

#i(t)
def RCi(t):
    ic=E0/R*np.exp(-t/(R*C))*HeavisideFunction(t)
    return ic

#プロット用の配列
dt=0.01
t=np.arange(-1, 10, dt)

#電源
E=E0*HeavisideFunction(t)

#v(t)
v=RCv(t)

#i(t)
i=RCi(t)

#グラフのサイズ
plt.figure(figsize=(16, 5))

#電圧プロット
plt.subplot(121)
plt.plot(t, E, color="blue", linewidth=2.5, linestyle="--", label=r"$E$")
plt.plot(t, v, color="red", linewidth=2.5, linestyle="-", label=r"$v(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='lower right')
#グラフの最大値・最小値
plt.xlim(-1, 10) #横軸の最大値・最小値
vmin=E.min() * 1.1
vmax=E.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

#電流プロット
plt.subplot(122)
plt.plot(t, i, color="red", linewidth=2.5, linestyle="-", label=r"$i(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Current [A]", fontsize=16)
plt.legend(loc='lower right')
#グラフの最大値・最小値
plt.xlim(-1, 10) #横軸の最大値・最小値
vmin=E.min() * 1.1
vmax=E.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

#調整用
#plt.subplots_adjust(wspace = 0.3) #プロット間の縦の調整

plt.show()
plt.savefig('graph.pdf')
