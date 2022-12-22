import matplotlib.pyplot as plt
import cmath
import numpy as np


def main():
    rion = 100 
    cfilm = 10
    dfilm = 0.1*0.01
    rfilm = 40 
    rct = 0.001
    L = 0.01*6
#    tlm = TLMB(rion, L, rfilm, cfilm, dfilm)

#    temp = tlm.Z(10000)
#    print(temp)

#    exit()
    for L in [ 0.01*i for i in range(1,8)]:
        TLMC(rion, L, rfilm, cfilm, dfilm, rct).plot_ColeCole()

    plt.show()

class TLMC:
    def __init__(self, rion, L, rfilm, cfilm, dfilm, rct):
        self.rion = rion
        self.L = L
        self.cfilm = cfilm
        self.rfilm = rfilm
        self.dfilm = dfilm
        self.rct = rct


    def Z(self, omega):
        ZA = self.rfilm
        YB = 1/self.rct + complex(0, self.cfilm*omega)
        ZB = 1/YB
        temp1 = cmath.sqrt(ZA*ZB)
        temp2 = self.dfilm*cmath.sqrt(ZA/ZB)
        Zfilm = temp1/cmath.tanh(temp2)
    
        ZA = self.rion
        ZB = Zfilm
        temp1 = cmath.sqrt(ZA*ZB)
        temp2 = self.L*cmath.sqrt(ZA/ZB)
        Ztot = temp1/cmath.tanh(temp2)

        return Ztot


    def plot_ColeCole(self):

#        freqs = [ 10**(i) for i in range(-2, 10)]
        freqs = [ 10**i for i in np.linspace(1, 100, 1000)]
        Zs = [ self.Z(f) for f in freqs ]

        Zs_real = [ z.real for z in Zs ]
        Zs_imag = [ -z.imag for z in Zs ]

        label = "rion={}, L={}, rfilm={}, cfilm={}, dfilm={}".format(self.rion, self.L, self.rfilm, self.cfilm, self.dfilm)
        plt.plot(Zs_real, Zs_imag, "o-", label=label)
        plt.xlim(0, 5)
        plt.ylim(0, 5)
        plt.legend()
#        plt.show()


    def plot_Bode(self):

        freqs = [ i for i in range(1, 100)]
        Zs = [ self.Z(f) for f in freqs ]
        Zs_abs = [ cmath.polar(z)[0] for z in Zs ]

        label = "rion={}, L={}, cfilm={}, dfilm={}".format(self.rion, self.L, self.cfilm, self.dfilm)
        plt.plot(freqs, Zs_abs, "o-", label=label)
        plt.xlim(0, 10)
        plt.ylim(0, 1)
        plt.legend()


class TLMB:
    def __init__(self, rion, L, rfilm, cfilm, dfilm):
        self.rion = rion
        self.L = L
        self.cfilm = cfilm
        self.rfilm = rfilm
        self.dfilm = dfilm


    def Z(self, omega):
        ZA = self.rfilm
        ZB = 1/complex(0, self.cfilm*omega)
        temp1 = cmath.sqrt(ZA*ZB)
        temp2 = self.dfilm*cmath.sqrt(ZA/ZB)
        Zfilm = temp1/cmath.tanh(temp2)
    
        ZA = self.rion
        ZB = Zfilm
        temp1 = cmath.sqrt(ZA*ZB)
        temp2 = self.L*cmath.sqrt(ZA/ZB)
        Ztot = temp1/cmath.tanh(temp2)

        return Ztot


    def plot_ColeCole(self):

#        freqs = [ 10**(i) for i in range(-2, 10)]
        freqs = [ 10**i for i in np.linspace(1, 100, 1000)]
        Zs = [ self.Z(f) for f in freqs ]

        Zs_real = [ z.real for z in Zs ]
        Zs_imag = [ -z.imag for z in Zs ]

        label = "rion={}, L={}, rfilm={}, cfilm={}, dfilm={}".format(self.rion, self.L, self.rfilm, self.cfilm, self.dfilm)
        plt.plot(Zs_real, Zs_imag, "o-", label=label)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.legend()
#        plt.show()


    def plot_Bode(self):

        freqs = [ i for i in range(1, 100)]
        Zs = [ self.Z(f) for f in freqs ]
        Zs_abs = [ cmath.polar(z)[0] for z in Zs ]

        label = "rion={}, L={}, cfilm={}, dfilm={}".format(self.rion, self.L, self.cfilm, self.dfilm)
        plt.plot(freqs, Zs_abs, "o-", label=label)
        plt.xlim(0, 10)
        plt.ylim(0, 1)
        plt.legend()



class TLMA: 

    def __init__(self, rion, cdl, L):

        self.rion = rion # ohm cm, resister per volume
        self. cdl = cdl # F cm^-3, capacitor
        self.L = L # cm, thickness of electrode


    def Z(self, omega):
        ZA = self.rion
        ZB = 1/complex(0, self.cdl*omega)
        temp1 = cmath.sqrt(ZA*ZB)
        temp2 = self.L*cmath.sqrt(ZA/ZB)
 #       print(ZA, ZB)

        return temp1/cmath.tanh(temp2)


    def plot_ColeCole(self):

#        freqs = [ 10**(i) for i in range(-2, 10)]
        freqs = [ i for i in range(1, 100000)]
        Zs = [ self.Z(f) for f in freqs ]

        Zs_real = [ z.real for z in Zs ]
        Zs_imag = [ -z.imag for z in Zs ]

        label = "rion={}, cdl={}, L={}".format(self.rion, self.cdl, self.L)
        plt.plot(Zs_real, Zs_imag, "o-", label=label)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.legend()
#        plt.show()


    def plot_Bode(self):

        freqs = [ i for i in range(1, 100)]
        Zs = [ self.Z(f) for f in freqs ]
        Zs_abs = [ cmath.polar(z)[0] for z in Zs ]

        label = "rion={}, cdl={}, L={}".format(self.rion, self.cdl, self.L)
        plt.plot(freqs, Zs_abs, "o-", label=label)
        plt.xlim(0, 10)
        plt.ylim(0, 1)
        plt.legend()

if __name__ == "__main__":
    main()
