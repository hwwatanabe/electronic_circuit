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

#プロット用の配列
dt=0.1
t=np.arange(-10, 10, dt)

#e(t)=cos(wt)
h=np.cos(w*t)

#v(t)
A=E0/(1+1.0j*R*C) #numpyでは虚数は1.0j
absA=np.abs(A)
angA=np.angle(A)
v=absA*np.cos(w*t+angA)

#プロット
plt.plot(t, h, color="blue", linewidth=2.5, linestyle="-", label=r"$e(t)$")
plt.plot(t, v, color="red", linewidth=2.5, linestyle="--", label=r"$v(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='upper left')
#グラフの最大値・最小値
plt.xlim(-10, 10) #横軸の最大値・最小値
#x軸の数値ラベル
plt.xticks(np.arange(-2*np.pi, 2.1*np.pi, np.pi),
            [r'$-2\pi$',r'$-\pi$',r'$0$',r'$\pi$',r'$2\pi$'],
            horizontalalignment = 'center',
            verticalalignment   = 'top',
            size = 15)
vmin=h.min() * 1.1
vmax=h.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる
plt.show()
plt.savefig('graph.pdf')
