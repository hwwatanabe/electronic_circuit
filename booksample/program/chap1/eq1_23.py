#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.ticker as ptick

#パラメタ
C=1.0  #[F]
w=1.0*(2*np.pi) #1[Hz]を[rad/s]に変換

#時間の配列作成
t=np.linspace(0, 4*np.pi/w, 256, endpoint=True)

#電圧と電流
v=np.sin(w*t)
i=w*np.sin(w*t+np.pi/2)

#電圧プロット
plt.subplot(211)
plt.plot(t, v, color="blue", linewidth=2.5, linestyle="-", label=r"$v(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='upper left')
#グラフの最大値・最小値
plt.xlim(t.min(), t.max()) #横軸の最大値・最小値
vmin=-v.max()*1.1
vmax=v.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

#電流プロット
plt.subplot(212)
plt.plot(t, i, color="red", linewidth=2.5, linestyle="-", label=r"$i(t)$")
#plt.plot(x, v, color="red", linewidth=1.5, linestyle="--", label="v(t)")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Current [A]", fontsize=16)
plt.legend(loc='upper left')
#グラフの最大値・最小値
plt.xlim(t.min(), t.max()) #横軸の最大値・最小値
imin=-i.max()*1.1
imax=i.max() * 1.1
plt.ylim(imin, imax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

plt.subplots_adjust(hspace = 0.3) #プロット間の縦の調整


#プロット
plt.show()
plt.savefig('graph.pdf')
