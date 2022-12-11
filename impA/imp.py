import cmath
import numpy as np 
import matplotlib.pyplot as plt

def main():

    Z = calc_imp(100)
    exit()

    reals = []
    imags = []
    for omega in  np.linspace(1, 1000, 100):
        Z = calc_imp(omega)
        reals.append(Z.real)
        imags.append(-Z.imag)
        print(omega, Z.real, Z.imag)
    
    plt.plot(reals, imags, "-o")
    plt.plot([0,1000], [0,1000] )
    plt.ylim(-0.1,5)
    plt.xlim(-0.1,5)
    plt.show()


def calc_imp(omega):
    Rcont = 1
    Rreact = 1000000
    Rion_liq = 1

    R1 = Rcont 
    R2 = 100000
    R3 = Rreact 
    R4 = Rreact 
    R5 = 0 
    R6 = Rion_liq
    R7 = 0 
    R8 = Rreact
    R9 = Rreact
    R10 = 1000000
    R11 = Rcont
    
    C1 = 0.01
    C2 = 0.01
    C3 = 0.01
    C4 = 0.01



    Z1 = calc_Z(omega, C1, R3)
    Z2 = calc_Z(omega, C2, R4)
    Z3 = calc_Z(omega, C3, R8)
    Z4 = calc_Z(omega, C4, R9)

    YY1 = 1/(Z1+R5) + 1/(Z2+R2)
    YY2 = 1/(Z3+R10) + 1/(Z4+R7)

    Ztot = R1 + 1/YY1 + R6 + 1/YY2 + R11
    print(Ztot)

    return Ztot



def calc_Z(omega, C,R):
    Y = complex(1/R, omega*C)
    return 1/Y

main()
