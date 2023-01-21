#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

#素子の値（値を変えて試してみてください）
w=1.0
R=1.0
C=1.0
E0=1.0

#プロット用の配列
dt=0.1
t=np.arange(-10, 10, dt)

#e(t)=E0
e0=E0*np.sin(w*t)

#v(t)
v=(1.0/np.sqrt(1.0+np.power(w*C*R,2.0)))*E0*np.cos(w*t-np.arctan(w*C*R))

#プロット
plt.plot(t, e0, color="blue", linewidth=2.5, linestyle="-", label="$e(t)$")
plt.plot(t, v, color="red", linewidth=2.5, linestyle="--", label="$v(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='upper left')
#グラフの最大値・最小値
plt.xlim(t.min(), t.max()) #横軸の最大値・最小値
vmin=e0.min() * 1.1
vmax=e0.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる
plt.rcParams["font.size"] = 16 #フォントサイズを一括で変更
plt.tight_layout() #画像のはみ出しを自動調整
plt.show()
plt.savefig('graph.pdf')
