#参考プログラム
#複素数の取扱（文字式）

from sympy import *

a, b, c, d = symbols('a b c d', real=True)  #実数で定義する
C=a+b*I
D=c+d*I
print("C=",C)
print("Re[C]=",re(C))
print("Im[C]=",im(C))
print("C*",conjugate(C))
print("r=",Abs(C))
print("theta=",arg(C))
