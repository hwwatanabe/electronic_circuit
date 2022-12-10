import numpy as np
import matplotlib.pyplot as plt


t = 0
dt = 0.0001
C = 0.001
R = 0.01
q =  0
V0 = 5 
omega = 100

qs = [q]
ts = [t]
i_s = [0]
Vs = [0]

V = lambda t: V0*np.sin(omega*t)
V = lambda t: V0

while(True):
    qprev = q

    t = t + dt

    ###
#    q = q + (-1*q/(C*R) + V)*dt
    a = (-1*q/(C*R) + V(t))
    b = (-1*(q+a*dt)/(C*R) + V(t+dt))
    q = q + 0.5*dt*(a+b)

    i = (q - qprev)/dt

    qs.append(q)
    ts.append(t)
    i_s.append(i)
    Vs.append(V(t))
    print(t,q, i)

    if t > 1/10:
        break

plt.plot(ts, i_s)
plt.plot(ts, Vs)
#plt.plot(Vs, i_s)
plt.ylim(-10, 10)
plt.axhline(0)
plt.show()

