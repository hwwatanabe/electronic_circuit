import matplotlib.pyplot as plt
import numpy as np
from modules import Boxel
import random

def main():

    nx = 20
    ny = 30
    dx = 0.1
    dy = 0.1
    dz = 1
    Boxel.set_parameter(nx, ny, dx, dy, dz)

#    ks = [random.uniform(1,10) for _ in range(Boxel.nboxel) ]
#    ks = [np.abs(random.gauss(mu=5,sigma=10)) for _ in range(Boxel.nboxel) ]
    ks = [random.uniform(1,1) for _ in range(Boxel.nboxel) ]
    Boxel.set_ks(ks)

    Boxel.set_ks_circle([18, 15], 0.5, 0.5)
    Boxel.set_ks_circle([10, 10], 0.8, 0.1)
    Boxel.set_ks_circle([ 8,  5], 0.2, 0.8)

    Boxel.run()

if __name__ == "__main__":
    main()
