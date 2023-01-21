# -*- coding: utf-8 -*-
import matplotlib
from oneDCircuit import oneDCircuit
from symOneDLine import symOneDLine
from Waves import SquareWave #信号源
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


###############################
#          伝送線路
#
# mtl = [[aii_1, d1j_1, r_1],
#        [aii_2, d1j_2, r_2], .....]
# mtl: 伝送線路の情報
# aii: 伝送線の半径
# d1j: 伝送線の距離（１本目からの）
# r: 伝送線の単位長さあたりの抵抗 ohm/m
###############################
lN = 2  #2で固定（このプログラムでは変更不可!）


#伝送線路の抵抗率
mtlR = Matrix([0.0,0.0])  #(1本目, 2本目)

l=2*25.4e-3   #長さ
Z0=124.0   #特性インピーダンス [Ohm]
TD=0.3e-9    #遅延時間[s]
Nx=50  #分割数

#プロットのパラメタ
x=np.linspace(0, l, Nx+1) #0-lの間にNx+1の配列をつくる

#伝送線のリスト
lstLn=[l,Nx,mtlR,lN,Z0,TD]


#伝送線路の初期化用リスト
ln=symOneDLine(lN, l, mtlR, Nx, Z0, TD)
dt=ln.dt
print('----------------------------')
print('dt=',dt)




###############################
#          ソース側
###############################
#素子
R1=124.0

#電源
E0 = symbols("E0", real=True)
#ここではsympyで定義して、
#あとでnumpyに変換している

#接続行列
A = Matrix([[1,0,1,0],
            [0,-1,0,1],
            [-1,1,0,0]])
#電流源
AJ = Matrix([0,0,0])

#電流源ベクトル
J = Matrix([0])

#電圧源ベクトル
E = Matrix([0,E0,0,0])

#インピーダンス行列
ZL = Matrix([[R1,0],
            [0,0]])

#デルタ行列（集中＋分布）
DLT = Matrix([[1,0],
              [0,1]])

#イプシロン行列（集中＋分布）
EPSLN = Matrix([[1,0],
                [0,1]])

#ソース側の初期化用リスト
lstSrc=[A,AJ,J,E,ZL,DLT,EPSLN]

###############################
#           負荷側
###############################
#素子
L=1.0e-7

#接続行列
AL = Matrix([[1,-1,0],
            [-1,0,-1]])
#電流源
AJL = Matrix([0,0])

#電流源ベクトル
JL = Matrix([0])

#電圧源ベクトル
EL = Matrix([0,0,0,0])

#インピーダンス行列
ZLL = Matrix([(2.0*L)/dt])

#デルタ行列（集中＋分布）
DLTL = Matrix([-1])

#イプシロン行列（集中）
EPSLNL = Matrix([1])

#負荷側の初期化用リスト
lstLd=[AL,AJL,JL,EL,ZLL,DLTL,EPSLNL]


###############################
#     １次元伝送線回路の初期化
###############################
cr = oneDCircuit(lstLn, lstSrc, lstLd)

#ソース側電源
PeriodTime=20.0e-9
PeriodInt=int(PeriodTime/dt)
SW=SquareWave(1.0, PeriodTime/2.0, PeriodTime, dt)   #パルス幅を決める
# 電源ベクトルのsympy => numpyへの変換
#self.E0 = symbols("E0", real=True)
PW=lambdify(cr.E0, cr.srcEJ, "numpy")
#電源ベクトルの初期化
PW1=PW(0.0)
PW0=PW(0.0)


# 伝送線路計算
def calcLines(i, cr):
    global PW1, PW0, PeriodInt
    global SW
    # 電源
    if (i<PeriodInt):
        #E1=SW[i]
        E1=1.0
    else:
        E1=0.0
    #PW1=PW(E1)   # １回のパルス
    PW1=PW(SW[np.mod(i, PeriodInt)])   # 繰り返しパルス

    #ソース側境界の計算
    cr.srcUI0[cr.src_num0:cr.src_num1,0] = cr.srcUI0[cr.src_num0:cr.src_num1,0] - 2.0*cr.Id0[:,1]
    cr.srcUI1 = -cr.srcP.dot(cr.srcUI0)+cr.srcInvC.dot(PW1+PW0)

    #負荷側境界の計算
    cr.ldUI0[cr.ld_num0:cr.ld_num1,0] = cr.ldUI0[cr.ld_num0:cr.ld_num1,0] - 2.0*cr.Id0[:,cr.N]
    cr.ldUI1 = -cr.ldP.dot(cr.ldUI0)

    # 境界での計算結果を伝送線路の境界に代入
    cr.Ud1[:,0] = cr.srcUI1[0:cr.lineNumber,0]
    cr.Id1[:,0] = cr.srcUI1[cr.src_num0:cr.src_num1,0]
    cr.Ud1[:,cr.N] = cr.ldUI1[0:cr.lineNumber,0]
    cr.Id1[:,cr.N+1] = cr.ldUI1[cr.ld_num0:cr.ld_num1,0]

    # 伝送線路の計算
    cr.Ud1[:,1:cr.N]=-cr.txP.dot(cr.Id0[:,2:cr.N+1]-cr.Id0[:,1:cr.N])+cr.Ud0[:,1:cr.N]
    cr.Id1[:,1:cr.N+1]=-cr.invLRp.dot(cr.Ud1[:,1:cr.N+1]-cr.Ud1[:,0:cr.N])+cr.invLRpLRm.dot(cr.Id0[:,1:cr.N+1])

    # 結果を１つ前の変数に代入
    cr.srcUI0 = cr.srcUI1
    cr.ldUI0 = cr.ldUI1
    cr.Ud0 = cr.Ud1
    cr.Id0 = cr.Id1
    PW0 = PW1

    #必要に応じて変更する
    #return np.float_(cr.Ud1[0]-cr.Ud1[1])
    #return PW1[1]
    return [PW1[1], np.float_(cr.Ud1[0]-cr.Ud1[1])]



##########################
#すべてを計算してからグラフに保存
##########################

ini_t=0.0
fin_t=40e-9
dtnum=int(fin_t/dt)
t=np.arange(ini_t, dtnum*dt, dt) #時間配列作成
et=np.zeros(t.size)
vt=np.zeros(t.size)


for i in range(dtnum):
    data = calcLines(i,cr)    # 計算
    print(i,"/",t.size,':', 'e(t)=', data[0][0], ' : v(t)=', data[1][Nx])
    et[0:t.size-1]=et[1:t.size]
    et[t.size-1]=data[0][0]
    vt[0:t.size-1]=vt[1:t.size]
    vt[t.size-1]=data[1][Nx]


#グラフ
#matplotlib.use("Agg")  #ここでなくても良い、必要な場合もある？
plt.plot(t, et, color="red",
    linewidth=1.5, linestyle="--", label="$e(t)$")    # グラフを生成
plt.plot(t, vt, color="blue",
    linewidth=1.5, linestyle="-", label="$v(t)$")    # グラフを生成

plt.xlabel("Time [s]", fontsize=16)
plt.ylabel("Voltage [V]", fontsize=16)
plt.legend(loc='upper right')
plt.tick_params(labelsize=14)
plt.xlim(0.0, fin_t)            #横軸の最大値・最小値
plt.ylim(-1.5, 2.0)         #縦軸の最大値・最小値
plt.grid(which="both")      #グリッドを入れる

plt.savefig('graph.pdf')    #画像保存


"""
##########################
#ある時間の画像を保存する場合
##########################
matplotlib.use("Agg")
oneShotInt=int(10e-9/dt)
vtt=[]
for i in range(oneShotInt):
    data = calcLines(i,cr)
    print(i, '/', oneShotInt, '=', data)
    vtt.append(data)

plt.plot(vtt, color="red",
      linewidth=1.5, linestyle="-", label="vc(t)")    # グラフを生成

#グラフの設定
plt.xlabel("Position ", fontsize=16)
plt.ylabel("V(t) [V]", fontsize=16)
plt.legend(loc='upper right')
plt.tick_params(labelsize=14)
plt.xlim(0.0, l)            #横軸の最大値・最小値
plt.ylim(-1.0, 1.0)         #縦軸の最大値・最小値
plt.grid(which="both")      #グリッドを入れる

plt.savefig('graph.pdf')    #画像保存
"""
