import matplotlib.pyplot as plt
import cmath
import numpy as np

def main():
    rion = 150 
    cfilm = 10 
    dfilm = 0.1*0.001

    rfilm = 80 
    rct = 0.001
    re = 50
    L = 0.01*6
#    tlm = TLMB(rion, L, rfilm, cfilm, dfilm)

#    temp = tlm.Z(10000)
#    print(temp)

#    exit()
    omegas = [2**i for i in range(-10, 30)]
    reals = []
    imags = []
    for omega in omegas:
        tlm = TLMCD(rion, L, rfilm, cfilm, dfilm, rct, re)
        ztot = tlm.Z(omega)
        reals.append(ztot.real)
        imags.append(-ztot.imag)


    plt.plot(reals, imags)
    plt.legend()
    plt.xlim(0,5)
    plt.ylim(0,5)
    plt.show()

class TLMCD:
    def __init__(self, rion, L, rfilm, cfilm, dfilm, rct, re):
        self.rion = rion
        self.L = L
        self.cfilm = cfilm
        self.rfilm = rfilm
        self.dfilm = dfilm
        self.rct = rct
        self.re   = re

        self.tlmd = TLMD(rion=self.rion, L=self.dfilm, re=self.re, cdl=self.cfilm)


    def Z(self, omega):
        ZA = self.rfilm
#        YB = 1/self.rct + complex(0, self.cfilm*omega)
        YB = complex(0, self.cfilm*omega)
        ZB = 1/YB
        temp1 = cmath.sqrt(ZA*ZB)
        temp2 = self.dfilm*cmath.sqrt(ZA/ZB)
        Zfilm = temp1/cmath.tanh(temp2)
    
        ZA = self.rion
        ZB = self.tlmd.Z(omega) 
        temp1 = cmath.sqrt(ZA*ZB)
        temp2 = self.L*cmath.sqrt(ZA/ZB)
        Ztot = temp1/cmath.tanh(temp2)

        return Ztot


class TLMD:
    def __init__(self, rion, L, cdl, re):
        self.rion = rion
        self.cdl  = cdl
        self.re   = re
        self.L    = L

    def Z(self, omega):
        za = self.rion
        zb = 1/(1j*omega*self.cdl)
        zc = self.re

        temp1 = (za*zc)/(za+zc)*self.L
        temp2 = cmath.sqrt(zb)/(za + zc)**(3/2)
        beta  = self.L*cmath.sqrt((za + zc)/zb)
        temp3 = (za**2 + zc**2)*cmath.cosh(beta) + 2*za*zc
        temp4 = cmath.sinh(beta)

        ztot = temp1 + temp2*temp3/temp4

        return ztot

if __name__ == "__main__":
    main()
