#!/usr/bin/env python
# -*- coding: utf-8 -*-

#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps

R=2.0
x1=np.linspace(0, 0.9, 10, endpoint=True)
p1=R*np.power(x1,2)
w1=R*np.power(x1,3)/3.0
x2=np.linspace(1, 2.9, 20, endpoint=True)
p2=R*np.power(x2-2,2)
w2=R*np.power(x2-2,3)/3.0+4.0/3.0
x3=np.linspace(3, 4, 11, endpoint=True)
p3=R*np.power(x3-4,2)
w3=R*np.power(x3-4,3)/3.0+8.0/3.0

#配列要素の結合
x=np.concatenate((x1, x2, x3), axis=0)
p=np.concatenate((p1, p2, p3), axis=0)
w=np.concatenate((w1, w2, w3), axis=0)

#プロット
plt.subplot(211)
plt.plot(x, p, color="blue", linewidth=2.5, linestyle="-", label=r"$p(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Power [J/s]", fontsize=16)
plt.legend(loc='upper left')

#グラフの最大値・最小値
plt.xlim(x.min(), x.max()) #横軸の最大値・最小値
pmin=-p.max()*0.1
pmax=p.max() * 1.1
plt.ylim(pmin, pmax) #縦軸の最大値・最小値
plt.vlines([1, 2, 3], pmin, pmax, linestyles="dashed")
plt.hlines([0,2], x.min(), x.max(), linestyles="dashed")

plt.subplot(212)
plt.plot(x, w, color="blue", linewidth=2.5, linestyle="-", label=r"$W(0,t)$")
#plt.plot(x, v, color="red", linewidth=1.5, linestyle="--", label="v(t)")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Energy [J]", fontsize=16)
plt.legend(loc='upper left')

#グラフの最大値・最小値
plt.xlim(x.min(), x.max()) #横軸の最大値・最小値
wmin=-w.max()*0.1
wmax=w.max() * 1.1
plt.ylim(wmin, wmax) #縦軸の最大値・最小値
plt.vlines([1, 2, 3], wmin, wmax, linestyles="dashed")
plt.hlines([0, 4.0/3.0, 8.0/3.0], x.min(), x.max(), linestyles="dashed")

plt.subplots_adjust(hspace = 0.3) #プロット間の縦の調整

#
plt.show()
plt.savefig('graph.pdf')
