#微分方程式
#¥frac{dv(t)}{dt}+¥frac{1}{RC}v(t)=E0
#を解く

#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

#ヘビサイド関数
def HeavisideFunction(t):
    return 0.5 * (np.sign(np.round(t,10)) + 1)


#素子の値
R=1.0
C=1.0
E0=1.0
v0=0.0

#プロット用の配列
dt=0.1
t=np.arange(-10, 10, dt)

#e(t)=E0
h=HeavisideFunction(t)
#v(t)
v=E0*(1-np.exp(-t/(R*C)))*h

#プロット
plt.plot(t, h, color="blue", linewidth=2.5, linestyle="-", label=r"$e(t)$")
plt.plot(t, v, color="red", linewidth=2.5, linestyle="--", label=r"$v(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='upper left')
#グラフの最大値・最小値
plt.xlim(t.min(), t.max()) #横軸の最大値・最小値
vmin=-0.1
vmax=v.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる
plt.rcParams["font.size"] = 16 #フォントサイズを一括で変更
plt.tight_layout() #画像のはみ出しを自動調整
plt.show()
plt.savefig('graph.pdf')
