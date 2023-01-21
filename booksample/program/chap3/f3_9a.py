#!/usr/bin/env python
# -*- coding: utf-8 -*-

#以下の２行はファイルの保存で必要
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

#グラフを書くときのデータ作成
x=np.linspace(0, 5*np.pi, 256, endpoint=True)
phi=np.pi/6
v=np.cos(x+phi)
psi=np.pi/6+np.pi/4
i=np.cos(x+psi)
p=v*i

#プロット
plt.plot(x, p, color="blue", linewidth=2.0, linestyle="-", label=r"$p(t)$")
plt.plot(x, v, color="red", linewidth=2.0, linestyle="--", label=r"$v(t)$")
plt.plot(x, i, color="red", linewidth=2.0, linestyle="-.", label=r"$i(t)$")
plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Power [J/s] or Voltage [V] or Current [A]", fontsize=16)
plt.legend(loc='lower right', fontsize=16) #ラベルの表示
plt.xlim(x.min(), x.max()) #横軸の最大値・最小値
plt.ylim(-v.max() * 1.1, v.max() * 1.1) #縦軸の最大値・最小値
plt.hlines(0, x.min(), x.max(),linewidth=1.0, linestyles="-") #y=0に線をひく
#plt.grid(which='major',color='black',linestyle='--')

#消費電力cos(phi-psi)に線を引く
plt.hlines(np.cos(phi-psi)/2.0, x.min(), x.max(),
            linewidth=0.5, linestyles="--")
#p(t)>0の領域に色を塗る
plt.fill_between(x,p,0,where=p>0, facecolor='black',
                 alpha=0.5)
#p(t)<0の領域に色を塗る
plt.fill_between(x,p,0,where=p<0, facecolor='black',
                 alpha=0.1)

plt.show()
plt.savefig('graph.pdf')
