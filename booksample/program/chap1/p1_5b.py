#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

#ヘビサイド関数
def HeavisideFunction(t):
    return 0.5 * (np.sign(np.round(t,10)) + 1)

#elements
C=1.0  #[F]
dt = 0.01  #[s] この値をいろいろ変えてみてください

#time array
t1=np.arange(-1, 1, dt)
v=HeavisideFunction(t1)
t2=np.arange(-1+dt/2.0, 1-dt/2.0, dt)
i=C*np.diff(v)/dt

#電圧プロット
plt.subplot(211)
plt.plot(t1, v, color="blue", linewidth=2.5, linestyle="-", label=r"$v(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='upper left')
#グラフの最大値・最小値
plt.xlim(t1.min(), t1.max()) #横軸の最大値・最小値
vmin=-v.max()*0.1
vmax=v.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

#電流プロット
plt.subplot(212)
plt.plot(t2, i, color="red", linewidth=2.5, linestyle="-", label=r"$i(t)$")
#plt.plot(x, v, color="red", linewidth=1.5, linestyle="--", label="v(t)")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Current [A]", fontsize=16)
plt.legend(loc='upper left')
#グラフの最大値・最小値
plt.xlim(t2.min(), t2.max()) #横軸の最大値・最小値
imin=-i.max()*0.1
imax=i.max() * 1.1
plt.ylim(imin, imax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

plt.subplots_adjust(hspace = 0.3) #プロット間の縦の調整


#プロット
plt.show()
plt.savefig('graph.pdf')
