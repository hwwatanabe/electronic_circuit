import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import inv
#import plotly.graph_objects as go

# todo, display V I k in one window


class Boxel:

    nboxel         = 0
    nx, ny         = 0, 0
    dx, dy, dz     = 0, 0, 0
    boxels         = []
    incidence_mat  = []
    R_mat          = []
    V_top          = 10
    V_bottom       = 4 
    left_mat       = []
    right_vec      = []
    result         = []
    elements       = []
    V_vec          = []
    I_vec          = []
    Lx             = 0
    Ly             = 0


    def __init__(self, ix, iy):
        cls = type(self)

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

        cls.nboxel += 1


    def set_idxs(self):
        cls = type(self)

        ix = self.ix
        iy = self.iy
        nx = cls.nx
        ny = cls.ny

        self.idx   = cls.make_idx(ix, iy)

        self.right = cls.make_idx( (ix+1)%nx, iy)
        self.left  = cls.make_idx( (ix-1)%nx, iy)

        if iy + 1 < ny:
            self.up    = cls.make_idx( ix, iy+1)
        else:
            self.up    = -1

        if iy - 1 > 0:
            self.down  = cls.make_idx( ix, iy-1)
        else:
            self.down  = -1


    @classmethod
    def set_ks(cls, ks):

        for bx, k in zip(cls.boxels, ks):
            bx.set_k(k)
#            print(bx.R)

    @classmethod
    def set_ks_circle(cls, center, radius, k):

        idx0 = cls.make_idx(center[0], center[1])
        for bx in cls.boxels:
            posx0 = cls.dx/2 + cls.boxels[idx0].ix*cls.dx
            posy0 = cls.dy/2 + cls.boxels[idx0].iy*cls.dy
            posx = cls.dx/2 + bx.ix*cls.dx
            posy = cls.dy/2 + bx.iy*cls.dy
            deltax = posx - (posx0 + cls.Lx*round((posx-posx0)/cls.Lx))
            deltay = posy - posy0
            d2 = deltax**2 + deltay**2

            if d2 < radius**2:
                bx.set_k(k)


    def set_k(self, k):
        cls = type(self)
        self.k = k

        if self.k != 0:
            self.R = 1/self.k/cls.dz  ## <- if dx == dy
        else:
            self.R = float("inf")


    @classmethod
    def make_idx(cls, ix, iy):

        idx = ix + iy*cls.nx

        return idx 

    @classmethod
    def decode_idx(cls, idx):
        ix = idx % cls.nx
        iy = int((idx - ix)/cls.nx)

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

        cls.Lx      = cls.dx*cls.nx
        cls.Ly      = cls.dy*cls.ny

        cls.generate_boxels()


    @classmethod
    def generate_boxels(cls):

        k = 1
        for iy in range(cls.ny):
            for ix in range(cls.nx):
                bx = cls(ix, iy)
                bx.set_idxs()
    
                cls.boxels.append(bx)

    class Element:
        def __init__(self, idx, direction, forward, backward, R):
            self.idx       = idx
            self.direction = direction # "x" or "y" 
            self.forward   = forward
            self.backward  = backward
            self.R         = R


    @classmethod
    def set_incidence_matrix(cls):

        mat = np.zeros((cls.nnode, cls.nelement))
        Rs  = []
        ielement = 0
        for bx in cls.boxels:

            if bx.iy == 0: # bottom, only up
                mat[bx.idx, ielement] =  1
                mat[bx.up , ielement] = -1
                Rave = (bx.R + cls.boxels[bx.up].R)/2
                Rs.append(Rave)

                e = cls.Element(ielement, "y", bx.up, bx.idx, Rave)
                cls.elements.append(e)

                ielement += 1

            
            elif bx.iy == cls.ny - 1: #  top, none
                pass

            else:

                mat[bx.idx   , ielement] =  1
                mat[bx.right , ielement] = -1

                Rave = (bx.R + cls.boxels[bx.right].R)/2
                Rs.append(Rave)

                e = cls.Element(ielement, "x", bx.right, bx.idx, Rave)
                cls.elements.append(e)

                ielement += 1

                mat[bx.idx, ielement] =  1
                mat[bx.up , ielement] = -1

                Rave = (bx.R + cls.boxels[bx.up].R)/2
                Rs.append(Rave)

                e = cls.Element(ielement, "y", bx.up, bx.idx, Rave)
                cls.elements.append(e)

                ielement += 1

        cls.incidence_mat = mat
        cls.R_mat         = np.diag(Rs)

#        print("-> element")
#        print("Y point")
#        print(mat)
#        print(np.linalg.matrix_rank(mat))


    @classmethod
    def set_eq(cls):

        mat0 = cls.incidence_mat[:cls.nx                 ,:].copy()
        mat1 = cls.incidence_mat[cls.nx:cls.nnode-cls.nx:,:].copy()
        mat2 = cls.incidence_mat[cls.nnode-cls.nx:       ,:].copy()
        zero_mat = np.zeros((mat1.shape[0], mat1.shape[0]))

        cls.left_mat = np.block([[mat1.T, cls.R_mat], [zero_mat, mat1]])

        temp1 = -1 * mat0.T @ np.ones(cls.nx)*cls.V_bottom
        temp2 = -1 * mat2.T @ np.ones(cls.nx)*cls.V_top
        temp3 = np.zeros(cls.nnode - 2*cls.nx)

        cls.right_vec = np.hstack((temp1+temp2, temp3))


    @classmethod
    def solve(cls):

        cls.result = inv(cls.left_mat) @ cls.right_vec
        cls.V_vec  = cls.result[:cls.nboxel-2*cls.nx]
        cls.I_vec  = cls.result[cls.nboxel-2*cls.nx:]
#        print(cls.result)
#        print(cls.V_vec)
#        print(cls.I_vec)


    @classmethod
    def display_model(cls):
        xs = []
        ys = []
        for bx in cls.boxels:
            xs.append(bx.ix)
            ys.append(bx.iy)
            
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_aspect("equal")
        ax1.scatter(xs, ys, color="black", s=3)

        for i in range(cls.nx):
            ax1.plot([i,i], [0,cls.ny-1], color="black")

        for i in range(1,cls.ny-1):
            ax1.plot([0, cls.nx], [i,i], color="black")
        plt.show()


    @classmethod
    def display_k(cls):
        xs = []
        ys = []
        ks = []
        ks = np.zeros((cls.ny, cls.nx))
        for bx in cls.boxels:
            ks[bx.iy, bx.ix] = bx.k

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_aspect("equal")
        im = ax1.imshow(ks, "jet")
        ax1.invert_yaxis()
        fig.colorbar(im, ax=ax1)
        plt.show()


    @classmethod
    def display_V(cls):
        xs = []
        ys = []
        Vs = np.zeros((cls.ny, cls.nx))
        cnt = 0
        for bx in cls.boxels:
            if bx.iy == 0:
                Vs[bx.iy, bx.ix] = cls.V_bottom 
                bx.V = cls.V_bottom
            elif bx.iy == cls.ny - 1:
                Vs[bx.iy, bx.ix] = cls.V_top 
                bx.V = cls.V_top
            else:
                Vs[bx.iy, bx.ix] = cls.V_vec[cnt]
                bx.V = cls.V_vec[cnt]
                cnt += 1

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_aspect("equal")
        im = ax1.imshow(Vs, "jet")
        ax1.invert_yaxis()
        fig.colorbar(im, ax=ax1)
        plt.show()


    @classmethod
    def display_I(cls):

        for e in cls.elements:
            if e.direction == "x":
                cls.boxels[e.forward].Ix += cls.I_vec[e.idx]/2
                cls.boxels[e.backward].Ix += cls.I_vec[e.idx]/2

            elif e.direction == "y":
                if cls.boxels[e.backward].iy == 0:
                    cls.boxels[e.backward].Iy += cls.I_vec[e.idx]
                else:
                    cls.boxels[e.backward].Iy += cls.I_vec[e.idx]/2

                if cls.boxels[e.forward].iy == cls.ny-1:
                    cls.boxels[e.forward].Iy += cls.I_vec[e.idx]
                else:
                    cls.boxels[e.forward].Iy += cls.I_vec[e.idx]/2

            else:
                print("e.direction is unknown, exit")
                exit()

        
        xs = []
        ys = []
        Ixs = np.zeros((cls.ny, cls.nx))
        Iys = np.zeros((cls.ny, cls.nx))
        Is  = np.zeros((cls.ny, cls.nx))
        for bx in cls.boxels:
            Ixs[bx.iy, bx.ix] = bx.Ix
            Iys[bx.iy, bx.ix] = bx.Iy
            Is[bx.iy , bx.ix] = np.sqrt(bx.Ix**2 + bx.Iy**2)


        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_aspect("equal")
        im = ax1.imshow(Is, "jet")
        ax1.invert_yaxis()
        fig.colorbar(im, ax=ax1)
        plt.show()


    @classmethod
    def run(cls):
        cls.set_incidence_matrix()
        cls.set_eq()
        cls.solve()
        cls.display_model()
        cls.display_k()
        cls.display_V()
        cls.display_I()


if __name__ == "__main__":
    main()
