import matplotlib.pyplot as plt
import numpy as np

class Boxel:

    def __init__(self, ix, iy, dx, dy, dz):
        self.ix  = ix 
        self.iy  = iy 
        self.idx = -1 


        self.dx = dx 
        self.dy = dy 
        self.dz = dz 

        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0

        self.V = 0
        self.Ix = 0
        self.Iy = 0


    def set_idxs(self, nx, ny):

        ix = self.ix
        iy = self.iy

        self.idx   = Boxel.make_idx(ix, iy, nx)

        self.right = Boxel.make_idx( (ix+1)%nx, iy, nx)
        self.left  = Boxel.make_idx( (ix-1)%nx, iy, nx)

        if iy + 1 < ny:
            self.up    = Boxel.make_idx( ix, iy+1, nx)
        else:
            self.up    = -1

        if iy - 1 > 0:
            self.down  = Boxel.make_idx( ix, iy-1, nx)
        else:
            self.down  = -1

        return 0

    def set_k(self, k):
        self.k = k
        self.R = 1/self.k/self.dz 

        return 0

    @staticmethod
    def make_idx(ix, iy, nx):
        idx = ix + iy*nx

        return idx 

    @staticmethod
    def decode_idx(idx, nx):
        ix = idx % nx
        iy = int((idx - ix)/nx)

        return [ix, iy]



class Model:

    def __init__(self, nx, ny):
        self.nx = nx
        self.ny = ny


    def read_boxels(self, boxels):
        self.boxels = boxels

        return 0


    def get_incidence_matrix(self):

        mat = np.zeros((nx, ny))
        for bx in boxels:
            pass

    def display_model(self):
        pass



if __name__ == "__main__":
    main()
