import numpy as np 
from modules import Point, Element, Model
import matplotlib.pyplot as plt
import random
from TLMC import TLMC


def main():

    N = 100 
    L = 1 
    model = Model(N, L)

#    ZAs = [lambda omega: L/N]*N
    ZAs = [lambda omega: L/N*(i/N) for i in range(1, N+1) ]

#    ZBs = [lambda omega: 1/(1j*omega*1*(1/N*L))]*(N+1)

    ZBs = [lambda omega: 1/(1j*omega*(1*L/N)) for i in range(1, N+2)]

    ZBs = []
    for i in range(1, N+2):

        if i % 2 == 0:
            rion = 100
            cfilm = 10
            dfilm = 0.1*0.01
            rfilm = 100*5
            rct = 0.001*10**18
            L = 0.01*6*10
            tlm = TLMC(rion, L, rfilm, cfilm, dfilm, rct)
            temp = lambda omega: tlm.Z(omega)

        else:
            temp = lambda omega: 1/(1j*omega*(1*L/N))

        ZBs.append(temp)

    ZA_tot = L/2*(1+1/N)
    model.set_Zs(ZAs, ZBs)

    omegas = [ 2**i for i in range(-100, 100)]
    reals = []
    imags = []
    for omega in omegas:
        print(omega)
        Ztot = model.get_Ztot(omega)
        reals.append(Ztot.real)
        imags.append(-Ztot.imag)

    plt.plot(reals, imags, "o-")
    plt.xlim(0,5)
    plt.ylim(0,5)
#    plt.aspect("equal")
    plt.show()




if __name__ == "__main__":
    main()
