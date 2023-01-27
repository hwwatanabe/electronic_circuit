import matplotlib.pyplot as plt
import numpy as np
from modules import Boxel
import random

def main():

    nx = 2 
    ny = 3 
    dx = 0.1
    dy = 0.1
    dz = 1
    Boxel.set_parameter(nx, ny, dx, dy, dz)
#    ks = [random.uniform(1,10) for _ in range(Boxel.nboxel) ]
    ks = [random.uniform(1,1) for _ in range(Boxel.nboxel) ]
    Boxel.set_ks(ks)
    Boxel.run()

if __name__ == "__main__":
    main()
