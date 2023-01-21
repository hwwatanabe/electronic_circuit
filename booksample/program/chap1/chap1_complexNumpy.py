#参考プログラム
#複素数の取扱
import numpy as np

#numpyでの複素数の利用
a=1.0   #実部
b=-1.0   #虚部
C1=a+b*1.0j
print("--------------------------------------")
print('C1=',C1)
print('Re[C1]=',np.real(C1))
print('Im[C1]=',np.imag(C1))
print('C1*=',np.conj(C1))
print('r1=',np.abs(C1))
print('angleC=',np.angle(C1, deg=True))   #deg=Trueで度数表示

print("--------------------------------------")
#偏角の式の確認
c=2.0*np.sqrt(3)
d=2.0
C2=c+d*1.0j


print('C1=',C1)
print('C2=',C2)
print('|C1|=', np.abs(C1))
print('|C2|=', np.abs(C2))

angleC1=np.angle(C1, deg=True)
angleC2=np.angle(C2, deg=True)
print('angleC1=', angleC1)
print('angleC2=', angleC2)
print('|C1/C2|=',np.abs(C1)/np.abs(C2))
print("angleC1-angleC2=", angleC1-angleC2)
print("angle(C1/C2)=", np.angle(C1/C2, deg=True))
print("--------------------------------------")
print("")
