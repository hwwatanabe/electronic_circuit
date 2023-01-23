import matplotlib.pyplot as plt
import numpy as np
from modules import Boxel

def main():

    nx = 2
    ny = 3
    dx = 0.1
    dy = 0.1
    dz = 1
    Boxel.set_parameter(nx, ny, dx, dy, dz)
    Boxel.run()

if __name__ == "__main__":
    main()
