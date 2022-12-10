import numpy as np 
import matplotlib.pyplot as plt
from numpy.linalg import solve


R1 = 1
R2 = 0.1
R3 = 1 
R4 = 1 
R5 = 0.1 
R6 = 10
R7 = 1

C1 = 0.1
C2 = 0.01
C3 = 0.1
C4 = 0.01

dt = 0.0001
V0 = 1
omega = 100
V = lambda t: V0*np.sin(omega*t)
#V = lambda t: V0 + 0*np.sin(t)

t = 0
q1 = 0
q2 = 0
q3 = 0
q4 = 0

ts = [0]
itots = [0]
i1s = [0]
i2s = [0]
q1s = [0]

while True:
    q1_prev = q1
    q2_prev = q2
    q3_prev = q3
    q4_prev = q4

    t += dt

    if t > 0.3:
        break

    temp = (R1 + R4 + R7)/2
    left = [
            [1,1,-1,-1],
            [R3, -R2, 0, 0],
            [0, 0, R6, -R5],
            [temp+R3/2, temp+R2/2, temp+R6/2, temp+R5/2]
            ]

        
    qc1 = q1/C1
    qc2 = q2/C2
    qc3 = q3/C3
    qc4 = q4/C4
    right = [0, -qc1+qc2, -qc3+qc4, V(t)-(qc1+qc2+qc3+qc4)/2]


    ans = solve(left, right)

    q1 += ans[0]*dt
    q2 += ans[1]*dt
    q3 += ans[2]*dt
    q4 += ans[3]*dt



    i1 = (q1 - q1_prev)/dt
    i2 = (q2 - q2_prev)/dt
    itot = i1 + i2

    ts.append(t)
    itots.append(itot)
    i1s.append(i1)
    i2s.append(i2)
    q1s.append(q1)
    print(t, q1, q2, q3, q4, itot, i1, i2)


ts = np.array(ts)
plt.plot(ts, itots, "--", label="itot")
plt.plot(ts, i1s, "--", label="i1")
plt.plot(ts, i2s, "--", label="i2")
plt.plot(ts ,V(ts))
#plt.plot(ts, q1s)
plt.legend()
plt.axhline(0)
plt.show()


