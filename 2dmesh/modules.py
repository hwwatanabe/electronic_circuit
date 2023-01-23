import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import inv
# use plotly


class Boxel:

    nboxel = 0
    nx, ny = 0, 0
    dx, dy, dz = 0, 0, 0
    boxels = []
    incidence_mat = []
    R_mat = []
    V_top  = 1 
    V_bottom = 0 
    left_mat = []
    right_vec = []
    result = []


    def __init__(self, ix, iy):

        self.ix  = ix 
        self.iy  = iy 

        self.idx   = -1 
        self.left  = -1 
        self.right = -1
        self.up    = -1 
        self.down  = -1 

        self.V  = 0
        self.Ix = 0
        self.Iy = 0

        Boxel.nboxel += 1


    def set_idxs(self):

        ix = self.ix
        iy = self.iy
        nx = Boxel.nx
        ny = Boxel.ny

        self.idx   = Boxel.make_idx(ix, iy)

        self.right = Boxel.make_idx( (ix+1)%nx, iy)
        self.left  = Boxel.make_idx( (ix-1)%nx, iy)

        if iy + 1 < ny:
            self.up    = Boxel.make_idx( ix, iy+1)
        else:
            self.up    = -1

        if iy - 1 > 0:
            self.down  = Boxel.make_idx( ix, iy-1)
        else:
            self.down  = -1

        return 0


    def set_k(self, k):
        self.k = k
        self.R = 1/self.k/Boxel.dz  ## <- if dx == dy

        return 0

    @staticmethod
    def make_idx(ix, iy):
        idx = ix + iy*Boxel.nx

        return idx 

    @staticmethod
    def decode_idx(idx):
        ix = idx % Boxel.nx
        iy = int((idx - ix)/Boxel.nx)

        return [ix, iy]

    @classmethod
    def set_parameter(cls, nx, ny, dx, dy, dz):
        cls.nx = nx
        cls.ny = ny
        cls.dx = dx 
        cls.dy = dy 
        cls.dz = dz 

        cls.nelement = nx*(2*ny-3)
        cls.nnode    = nx*ny
        cls.nKCL     = cls.nnode - 1
        cls.nKVL     = cls.nelement - cls.nnode + 1

        return 0


    @classmethod
    def generate_boxels(cls):

        k = 1
        for iy in range(cls.ny):
            for ix in range(cls.nx):
                bx = Boxel(ix, iy)
                bx.set_idxs()
                bx.set_k(k)
    
                cls.boxels.append(bx)


    @classmethod
    def set_incidence_matrix(cls):

        mat = np.zeros((cls.nnode, cls.nelement))
        Rs  = []
        ielement = 0
#        print("bx.idx, bx.ix, bx.iy")
        for bx in cls.boxels:
#            print(bx.idx, bx.ix, bx.iy, ielement)

            if bx.iy == 0: # bottom, only up
                mat[bx.idx, ielement] =  1
                mat[bx.up , ielement] = -1

                Rave = (bx.R + cls.boxels[bx.up].R)/2
                Rs.append(Rave)

                ielement += 1

            
            elif bx.iy == cls.ny - 1: #  top, none
                pass

            else:

                mat[bx.idx   , ielement] =  1
                mat[bx.right , ielement] = -1

                Rave = (bx.R + cls.boxels[bx.right].R)/2
                Rs.append(Rave)

                ielement += 1

                mat[bx.idx, ielement] =  1
                mat[bx.up , ielement] = -1

                Rave = (bx.R + cls.boxels[bx.up].R)/2
                Rs.append(Rave)

                ielement += 1

        cls.incidence_mat = mat
        cls.R_mat         = np.diag(Rs)

        print("-> element")
        print("Y point")
        print(mat)
        print(cls.R_mat)
#        print(np.linalg.matrix_rank(mat))


    @classmethod
    def set_eq(cls):

        mat0 = cls.incidence_mat[:cls.nx                 ,:].copy()
        mat1 = cls.incidence_mat[cls.nx:cls.nnode-cls.nx:,:].copy()
        mat2 = cls.incidence_mat[cls.nnode-cls.nx:       ,:].copy()

        temp1 = np.vstack((cls.R_mat, mat1))

        zero_mat = np.zeros((mat1.shape[0], mat1.shape[0]))
        temp2    = np.vstack((mat1.T, zero_mat))

        cls.left_mat = np.hstack((temp2, temp1))

        temp1 = -1 * mat0.T @ np.ones(cls.nx)*cls.V_bottom
        temp2 = -1 * mat2.T @ np.ones(cls.nx)*cls.V_top
        temp3 = np.zeros(cls.nnode - 2*cls.nx)

        cls.right_vec = np.hstack((temp1+temp2, temp3))


    @classmethod
    def solve(cls):

        cls.result = inv(cls.left_mat) @ cls.right_vec
        print(cls.result)


    @classmethod
    def display_model(cls):
        # plotly
        pass

    @classmethod
    def run(cls):
        cls.generate_boxels()
        cls.set_incidence_matrix()
        cls.set_eq()
        cls.solve()

if __name__ == "__main__":
    main()