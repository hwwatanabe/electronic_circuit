import matplotlib.pyplot as plt
import numpy as np
from modules import Boxel, Model

def main():

    nx = 3 
    ny = 3 
    dx = 0.1
    dy = 0.1
    dz = 1
    k = 1

    nelement = nx*ny
    nnode    = nx*ny

    nKCL = nnode - 1
    nKVL = nelement - nnode + 1

    boxels = []
    for ix in range(nx):
        for iy in range(ny):
            bx = Boxel(ix, iy, dx, dy, dz)
            bx.set_idxs(nx, ny)
            bx.set_k(k)

            boxels.append(bx)

    idxs = []
    for bx in boxels:
        idxs.append(bx.idx)
#    print(sorted(idxs))
    print(idxs)
    exit()
        
    
    model = Model(nx, ny)
    model.read_boxels(boxels)


if __name__ == "__main__":
    main()
