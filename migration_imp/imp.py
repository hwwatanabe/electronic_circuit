import numpy as np 
from modules import Point, Element, Model
import matplotlib.pyplot as plt


def main():

    N = 5 
    L = 1
    model = Model(N, L)

    ZAs = [lambda omega: 1]*N
    ZBs = [lambda omega: 1/(1j*omega*1*0.1)]*(N+1)
    model.set_Zs(ZAs, ZBs)

    omegas = [ 2**i for i in range(-10, 10)]
    reals = []
    imags = []
    for omega in omegas:
        Ztot = model.get_Ztot(omega)
        reals.append(Ztot.real)
        imags.append(-Ztot.imag)

    plt.plot(reals, imags, "o-")
    plt.xlim(0,5)
    plt.ylim(0,5)
    plt.show()




if __name__ == "__main__":
    main()
