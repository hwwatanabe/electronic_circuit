#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

from sympy import *

#パラメタ
L=1.0  #[H]
w=1.0*(2*pi) #1[Hz]を[rad/s]に変換

#変数の定義
t0=symbols("t", real=True)   #変数はt0、表示はt
i0=sin(w*t0)   #電流の関数を定義している
v0=diff(i0,t0)   #i0をtで微分
print("v(t)=", v0)
print("i(t)=", i0)

v1=lambdify(t0, v0, "numpy")  #numpyの関数に変換
i1=lambdify(t0, i0, "numpy")

#時間の配列作成
t=np.linspace(0, 2, 256, endpoint=True)

#素子電圧と素子電流の配列を作成
v=v1(t)
i=i1(t)

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
