#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

v=3.0e8 #信号の速度
l=1.0 #伝送線の長さ

x=np.linspace(0, l, 256, endpoint=True)
theta=60.0*np.pi/180.0

f1=100e3
k1=2.0*np.pi*f1/v
v1=np.sin(k1*x+theta)

f2=100e6
k2=2.0*np.pi*f2/v
v2=np.sin(k2*x+theta)

#プロット
plt.plot(x, v1, color="blue", linewidth=2.5, linestyle="-", label=r"$v(x)$@100[kHz]")
plt.plot(x, v2, color="red", linewidth=2.5, linestyle="--", label=r"$v(x)$@100[MHz]")
plt.xlabel("x [m]", fontsize=16)
plt.ylabel("v(x) [V]", fontsize=16)

#グラフの最大値・最小値
plt.xlim(x.min(), x.max()) #横軸の最大値・最小値
plt.ylim(-0.1, 1.1) #縦軸の最大値・最小値
plt.grid(which="both")

#ラベルの表示
plt.legend(loc='upper right')

plt.show()
plt.savefig('graph.pdf')
