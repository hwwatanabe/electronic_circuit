import numpy as np
import matplotlib.pyplot as plt


t = 0
dt = 0.0001
C = 0.01
R = 1
q =  0
V0 = 5 
omega = 100

qs = [q]
ts = [t]
i_s = [0]
Vs = [0]

V = lambda t: V0*np.sin(omega*t)
#V = lambda t: V0
f = lambda t, q: -1*q/(C*R) + V(t)

while(True):
    qprev = q

    t = t + dt

    ###
#    q = q + (-1*q/(C*R) + V)*dt
    a = f(t,q) 
    b = f(t+0.5*dt, q+a*0.5*dt)
    c = f(t+0.5*dt, q+b*0.5*dt)
    d = f(t+dt, q+c*dt)
    q = q + dt/6*(a+2*b+2*c+d)

    i = (q - qprev)/dt

    qs.append(q)
    ts.append(t)
    i_s.append(i)
    Vs.append(V(t))
    print(t,q, i)

    if t > 5/10:
        break

print(max(i_s))
ts = np.array(ts)
plt.plot(ts, i_s)
plt.plot(ts, Vs)
#plt.plot(ts, V0/R*np.exp(-1*ts/(C*R)))
#plt.plot(Vs, i_s)
plt.ylim(-10, 10)
plt.axhline(0)
plt.show()

