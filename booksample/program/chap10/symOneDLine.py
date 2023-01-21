# -*- coding: utf-8 -*-
"""
1D Line
"""

import numpy as np
from sympy import *

###############################
# mtl = [aii, d1j, r]
# aii: radius of wire
# d1j: distance from the 1st line
# r: resistance ohm/m
###############################

class symOneDLine:
    # constant
    EPSILON_0=8.85418782e-12
    MU_0=1.25663706e-6
    PI=3.14159265359

    #matrices
    #constructor
    def __init__(self, lineNumber, lineLength, mtlR, N, Z0, TD):
        self.lineNumber = lineNumber
        self.lineLength = lineLength
        self.mtlR = mtlR
        self.N = N
        self.Z0 = Z0
        self.TD = TD

        # initialize lines
        self.lightVelocity = 1.0 / sqrt(self.EPSILON_0*self.MU_0)
        self.velocity = self.lineLength/self.TD
        self.dx=self.lineLength/self.N
        self.dt = self.dx/self.velocity

        # matrices
        self.Rmatrix = self.getLineRmatrix()
        self.Zmatrix = self.get1DCharacteristicZPLmatrix(0)
        self.Pmatrix = self.get1DCharacteristicZPLmatrix(1)
        self.Lmatrix = self.get1DCharacteristicZPLmatrix(2)
        self.LRpM = self.LRpluseMatrix()
        self.invLRpM = self.invLRpluseMatrix()
        self.LRmM = self.LRminusMatrix()
        self.invLRpLRmM = self.invLRpluseLRminusMatrix ()


    # distributed U vector
    def getUvec(self):
        U = zeros(self.lineNumber, self.N+1)
        return U

    # distributed U vector
    def getIvec(self):
        I = zeros(self.lineNumber, self.N+2)
        return I


    # (L/dt+R/2) matrix
    def LRpluseMatrix (self):
        return (self.Lmatrix/self.dt+self.Rmatrix/2.0)


    # inv(L/dt+R/2) matrix
    def invLRpluseMatrix (self):
        LR = self.LRpM
        return LR.inv()


    # (L/dt-R/2) matrix
    def LRminusMatrix (self):
        return (self.Lmatrix/self.dt-self.Rmatrix/2.0)


    # inv(L/dt+R/2)*(L/dt-R/2) matrix
    def invLRpluseLRminusMatrix (self):
        invLR = self.invLRpM
        LRminus = self.LRmM
        return invLR*LRminus

    #get line R matrix
    def getLineRmatrix(self):
        R = zeros(self.lineNumber, self.lineNumber)
        """for i in range(self.lineNumber):
            print('self.mtlR=',self.mtlR[i])
            R[i,i] = self.mtlR[i]
            print('R=',R[i,i])"""
        R[0,0] = self.mtlR[0]
        R[1,1] = self.mtlR[1]
        return R


    #for calculation Z, P, and L of 1D line
    # Z0P1L2=0 => return Z
    # Z0P1L2=1 => return P
    # Z0P1L2=2 => return L
    def get1DCharacteristicZPLmatrix (self, Z0P1L2):
        ZPL = zeros(self.lineNumber, self.lineNumber)
        if Z0P1L2==0:  # Z
            ZPL[0,0] = self.Z0/2.0
            ZPL[1,1] = self.Z0/2.0
        elif (Z0P1L2==1): #P
            ZPL[0,0] = self.Z0/2.0*self.lineLength/self.TD
            ZPL[1,1] = self.Z0/2.0*self.lineLength/self.TD
        else: #L
            ZPL[0,0] = self.Z0/2.0*self.TD/self.lineLength
            ZPL[1,1] = self.Z0/2.0*self.TD/self.lineLength

        return ZPL


# end of Lines class
