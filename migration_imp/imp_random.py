import numpy as np 
from modules import Point, Element, Model
import matplotlib.pyplot as plt
import random


def main():

    xs = []
    ys = []
    for i in range(5000):
        print(i)
        x, y = get_result()
        xs.append(x)
        ys.append(y)

    plt.scatter(xs, ys)
    plt.show()

    print(np.corrcoef([xs,ys]))


def get_result():
    N = 100 
    L = 1 
    model = Model(N, L)

#    ZAs = [lambda omega: L/N]*N
    ZAs = [lambda omega: random.normalvariate(L/N,L/N/5) for i in range(1, N+1) ]
#    ZBs = [lambda omega: 1/(1j*omega*1*(1/N*L))]*(N+1)
    ZBs = [lambda omega: 1/(1j*omega*(1*L/N)) for i in range(1, N+2)]
    model.set_Zs(ZAs, ZBs)

    ZA_tot = 0
    for z in ZAs:
        ZA_tot += z(0)

    Ztot = model.get_Ztot(omega=2**(-10))

    return [ZA_tot, Ztot.real]




if __name__ == "__main__":
    main()
