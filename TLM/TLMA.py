import matplotlib.pyplot as plt
import cmath


def main():
    rion = 20
    cdl = 100
    L = 0.01
    tlm = TLMA(rion, cdl, L)

    temp = tlm.Z(100)
    print(temp)
    for rion in [ 20*i for i in range(1,6)]:
#    for cdl in [ 100*i for i in range(1,6)]:
#    for L in [ 0.01*i for i in range(1,6)]:
#        TLMA(rion, cdl, L).plot_ColeCole()
        TLMA(rion, cdl, L).plot_Bode()

    plt.show()


class TLMB:
    def __init__(self, rion, cdl, L, rfilm, dfilm):
        pass


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
        freqs = [ i for i in range(1, 1000)]
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
