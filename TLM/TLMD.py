import cmath 
import matplotlib.pyplot as plt

def main():
    for re in [0, 10, 20, 30, 40, 50]:
        plot(re)

    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.legend()
    plt.show()

def plot(re):

    rion = 100 # ohm cm
    L = 0.01 # cm
#    re = 10 # ohm cm
    cdl = 100  # Fcm-3
    tlm = TLMD(rion=rion, L=L, cdl=cdl, re=re)

    omegas = [2**i for i in range(-10, 10)]
    reals = []
    imags = []
    for omega in omegas:
        ztot = tlm.Z(omega)
        reals.append(ztot.real)
        imags.append(-ztot.imag)

    plt.plot(reals, imags, label="re={}".format(re))




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
