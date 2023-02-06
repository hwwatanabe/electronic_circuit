import numpy as np 
from modules import Point, Element, Model
import matplotlib.pyplot as plt


def main():

    N = 100 
    L = 1 
    model = Model(N, L)

#    ZAs = [lambda omega: L/N]*N
    ZAs = [lambda omega: L/N*(i/N) for i in range(1, N+1) ]
#    ZBs = [lambda omega: 1/(1j*omega*1*(1/N*L))]*(N+1)
    ZBs = [lambda omega: 1/(1j*omega*(1*L/N)) for i in range(1, N+2)]
    ZA_tot = L/2*(1+1/N)
    model.set_Zs(ZAs, ZBs)

    omegas = [ 2**i for i in range(-10, 10)]
    reals = []
    imags = []
    for omega in omegas:
        print(omega)
        Ztot = model.get_Ztot(omega)
        reals.append(Ztot.real)
        imags.append(-Ztot.imag)

    plt.plot(reals, imags, "o-")
    plt.xlim(0,2)
    plt.ylim(0,2)
    plt.show()




if __name__ == "__main__":
    main()
