import numpy as np
import matplotlib.pyplot as plt


t = 0
dt = 0.001
C = 0.001
R = 1
q =  0
V0 = 5 
omega = 100

qs = [q]
ts = [t]
i_s = [0]
Vs = [0]
while(True):
    qprev = q
    V = V0*np.sin(omega*t)
    q = q + (-1*q/(C*R) + V)*dt
    t = t + dt
    i = (q - qprev)/dt

    qs.append(q)
    ts.append(t)
    i_s.append(i)
    Vs.append(V)
    print(t,q, i)

    if t > 1/10:
        break

plt.plot(ts, i_s)
plt.plot(ts, Vs)
#plt.plot(Vs, i_s)
plt.ylim(-10, 10)
plt.axhline(0)
plt.show()

