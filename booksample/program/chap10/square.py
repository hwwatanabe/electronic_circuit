#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

#パラメタ
a=1.0
b=3.0

#フーリエ級数で矩形波の配列を作成
def SquareWave(t,a,b):
    n=10000 #調整必要、通常はこれくらい？
    sw=a/(a+b)
    for i in range(n):
        sw += (2.0/(i+1)/np.pi)*np.sin((i+1)*a*np.pi/(a+b))*np.cos((t-a/2.0)*2.0*np.pi*(i+1)/(a+b))
    return sw

#プロット用の配列
dt=0.01
t=np.arange(-1, 10, dt)
print('t=',t)
sw1=SquareWave(t, a, b)
print('sw1=',sw1)


plt.plot(t, sw1, color="red", linewidth=2.5, linestyle="-", label="v(t)")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)

#プロットの調整
#グラフのサイズ
#plt.figure(figsize=(10, 5))

plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='lower right')
plt.tick_params(labelsize=14)
#グラフの最大値・最小値
plt.xlim(-1, 10) #横軸の最大値・最小値
vmin=sw1.min() * 1.1
vmax=sw1.max() * 1.1
plt.ylim(vmin, vmax) #縦軸の最大値・最小値
plt.grid(which="both") #グリッドを入れる

plt.show()
plt.savefig('graph.pdf')
