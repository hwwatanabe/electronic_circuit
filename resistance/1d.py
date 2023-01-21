import numpy as np
import matplotlib.pyplot as plt


def main():
    nmax = 10000
    jmax = 100
    xs = 0
    xe = 1
    dx = (xe-xs)/jmax

    x = np.linspace(xs, xe, jmax)
#    sigma = np.ones(jmax)
    sigma = [ 1.5 if 0.4 <= x[j] < 0.6 else 1 for j in range(jmax) ]
#    sigma = [ 0.5*(1-x[j]*(1-x[j])+0.01) for j in range(jmax) ]
#    sigma = [ np.tanh(x[j])+1 for j in range(jmax) ]

    phi = np.array([ 0 + (1-0)/(xe-xs)*x[j] for j in range(jmax)])
#    phi = x.copy()
    current = np.zeros(jmax)

    residual = np.zeros(nmax)

    for n in range(nmax):
        phiold = phi.copy()

        phi[0] =  0
        phi[jmax-1] = 1


        for j in range(1, jmax-1):
#            temp1 =  1/8*sigma[j+1] - 1/8*sigma[j-1] + 1/2
#            temp2 = -1/8*sigma[j+1] + 1/8*sigma[j-1] + 1/2
#            phi[j] = temp1*phi[j+1] + temp2*phi[j-1]
            
            temp1 = (phi[j+1] + phi[j-1])
            temp2 = (sigma[j+1] - sigma[j-1])*(phi[j+1] - phi[j-1])/4
            phi[j] = 0.5*(temp1 + temp2)

            current[j] = sigma[j]*(phi[j+1] - phi[j-1])/2/dx


        residual[n] = np.sqrt(((phi - phiold)**2).sum()/jmax)
        print(n, residual[n])


    plt.plot(x, phi)
    plt.plot(x[1:jmax-1], current[1:jmax-1])
#    plt.yscale("log")
    plt.show()

main()
