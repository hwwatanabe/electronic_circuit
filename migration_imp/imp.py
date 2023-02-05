import numpy as np 
from modules import Point, Element, Model


def main():
    N = 5 
    ZAs = [lambda omega: 1]*N
    ZBs = [lambda omega: 1/(1j*omega*1)]*(N+1)
    model = Model(N, 1)

    model.set_points()
    model.set_elements()
    model.set_connection_mat()
    model.set_Zs(ZAs, ZBs)
    model.set_Z_mat(omega=1)
    model.set_eq()
    model.solve()






if __name__ == "__main__":
    main()
