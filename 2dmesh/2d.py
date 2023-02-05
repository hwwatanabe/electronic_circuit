import matplotlib.pyplot as plt
import numpy as np
from modules import Boxel
import random

def main():

    nx = 50
    ny = 50 
    dx = 0.1
    dy = 0.1
    dz = 1

    Boxel.set_parameter(nx, ny, dx, dy, dz)
    ks = [random.uniform(0.1,1) for _ in range(Boxel.nboxel) ]
#    ks = [random.uniform(1,1) for _ in range(Boxel.nboxel) ]
    Boxel.set_ks(ks)
    Boxel.set_ks_circle([0, 25], 1.5, 0.00001)
    Boxel.run()
    Boxel.plot_all()
    exit()

    rs = np.linspace(0.1,3.5,25)
    ks = []
    cnt = 0
    for r in rs:
        cnt += 1
        print(cnt)
        ks.append(get_k(r))


    plt.plot(rs, ks)
    plt.show()


def get_k(r):
    nx = 50
    ny = 50 
    dx = 0.1
    dy = 0.1
    dz = 1

#    ks = [random.uniform(1,10) for _ in range(Boxel.nboxel) ]
    Boxel.set_parameter(nx, ny, dx, dy, dz)
    ks = [random.uniform(1,1) for _ in range(Boxel.nboxel) ]
    Boxel.set_ks(ks)
    Boxel.set_ks_circle([0, 25], r, 0.00001)
    Boxel.run()
#    Boxel.plot_all()

    return Boxel.ktot

if __name__ == "__main__":
    main()
