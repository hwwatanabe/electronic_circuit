import numpy as np 
import matplotlib.pyplot as plt


class Point:

    def __init__(self, idx):
        self.idx = idx
        self.V = 0


class Element:

    def __init__(self, idx, name, forward, backward):

        self.idx  = idx
        self.name = name

        self.forward  = forward  # Point 
        self.backward = backward # Point 

        self.I = 0

    def set_Z(self, Z):
        self.Z = Z # function

    def get_Z(self, omega):
        return self.Z(omega)


class Model:

    def __init__(self, N, L):
        self.N = N 
        self.L = L

        self.npoint   = N + 2 
        self.nelement = 2*N + 1 + 1
        self.points   = []
        self.elements = []

        self.connection_mat = np.zeros((self.npoint   , self.nelement), dtype=np.complex128)
        self.Z_mat          = np.zeros((self.nelement , self.nelement), dtype=np.complex128)
        self.zero_mat       = np.zeros((self.npoint-1   , self.npoint-1  ), dtype=np.complex128)

        self.left_mat  = None
        self.right_vec = None
        self.result    = None
        self.Ztot      = 0


        self.set_points()
        self.set_elements()
        self.set_connection_mat()


    def set_points(self):
        for idx in range(self.npoint):
            self.points.append(Point(idx))

    def set_elements(self):
        for idx in range(self.nelement):
            if  idx == 0:
                backward= self.points[idx          ]
                forward = self.points[self.npoint-1]
                self.elements.append(Element(idx, "E", forward, backward))

            elif 0 < idx < self.N + 1:
                forward  = self.points[idx+1-1]
                backward = self.points[idx+0-1]
                self.elements.append(Element(idx, "ZA", forward, backward))

            elif self.N + 1 <= idx < self.nelement:
                temp_idx = idx - self.N 
                forward  = self.points[self.npoint-1]
                backward = self.points[temp_idx-1]
                self.elements.append(Element(idx, "ZB", forward, backward))

            else:
                print("wrong element idx, exit")
                exit()


    def set_Zs(self, ZAs, ZBs):

        cnt_ZA = 0
        cnt_ZB = 0

        if len(ZAs) != self.N:
            print("len(ZAs) must be {}".format(self.N))
            exit()

        if len(ZBs) != self.N+1:
            print("len(ZAs) must be {}".format(self.N+1))
            exit()

        for idx in range(self.nelement):
            if self.elements[idx].name == "E":
                self.elements[idx].set_Z(lambda omega: 0)

            elif self.elements[idx].name == "ZA":
#                self.elements[idx].set_Z(lambda omega: 1)
                self.elements[idx].set_Z(ZAs[cnt_ZA])
                cnt_ZA += 1 

            elif self.elements[idx].name == "ZB":
#                self.elements[idx].set_Z(lambda omega: 1)
                self.elements[idx].set_Z(ZBs[cnt_ZB])
                cnt_ZB += 1 

            else:
                print("unknown element name, exit")
                exit()

    def set_connection_mat(self):
        for e in self.elements:
            self.connection_mat[e.forward.idx  ,e.idx] = -1
            self.connection_mat[e.backward.idx ,e.idx] =  1
#        print(self.connection_mat)

    def set_Z_mat(self, omega):
        for e in self.elements:
            self.Z_mat[e.idx, e.idx] = e.get_Z(omega)
#        print(self.Z_mat)

    def set_eq(self):
        connection_mat_r = self.connection_mat[:-1,:]
        a11 = connection_mat_r.T
        a12 = -self.Z_mat 
        a21 = self.zero_mat
        a22 = connection_mat_r

        self.left_mat  = np.block([[a11,a12],[a21,a22]])
        self.right_vec =  np.zeros(self.nelement + self.npoint - 1)
        self.right_vec[0] = 1 

#        print(self.left_mat)
#        print(self.right_vec)

    def solve(self):
        self.result = np.linalg.inv(self.left_mat) @ self.right_vec
#        print(self.result)

        self.result_V = self.result[:self.npoint-1]
        self.result_I = self.result[self.npoint-1:]
        print(self.result_V)
        print(self.result_I)

        for idx in range(self.npoint):
            if idx != self.npoint-1:
                self.points[idx].V = self.result_V[idx]
            else:
                self.points[idx].V = 0

        for idx in range(self.nelement):
            self.elements[idx].I = self.result_I[idx]

    def get_Ztot(self, omega):
        self.set_Z_mat(omega)
        self.set_eq()
        self.solve()
        self.Ztot = -1 * self.points[0].V / self.elements[0].I
#        print(self.Ztot)

        return self.Ztot


    def display(self):
        pass


if __name__ == "__main__":
    main()
