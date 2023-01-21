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
    def __init__(self, lineNumber, lineLength, mtl, N=100, epsilon_r=1.0, mu_r=1.0):
        self.lineNumber = lineNumber
        self.lineLength = lineLength
        self.mtl = mtl
        self.N = N
        self.epsilon_r = epsilon_r
        self.mu_r = mu_r

        # initialize lines
        self.lightVelocity = 1.0 / sqrt(self.EPSILON_0*self.MU_0)
        self.velocity = 1.0 / sqrt(self.EPSILON_0*self.MU_0*self.epsilon_r*self.mu_r)
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
        for i in range(self.lineNumber):
            R[i,i] = self.mtl[i,2]
        return R


    #for calculation Z, P, and L of 1D line
    # Z0P1L2=0 => return Z
    # Z0P1L2=1 => return P
    # Z0P1L2=2 => return L
    def get1DCharacteristicZPLmatrix (self, Z0P1L2):
        a=0.0
        ZPL = zeros(self.lineNumber, self.lineNumber)
        for i in range(self.lineNumber):
            for j in range(self.lineNumber):
                if i==j: a = float(self.mtl[i,0])  # self components
                else: a = Abs(float(self.mtl[i,1])-float(self.mtl[j,1]))  #mutual component
                ZPL[i,j] = ln(2.0*self.lineLength/a)-1.0

        keisu=0.0
        if Z0P1L2==0:  # Z
            keisu = (self.MU_0 * self.mu_r)/(2 * self.PI)/(2 * self.PI * self.EPSILON_0 * self.epsilon_r)
            #ZPL1=sqrt(ZPL*ZPL*keisu)
            ZPL1=simplify(ZPL*sqrt(keisu)) #正しい？
        elif (Z0P1L2==1): #P
            keisu = 1/(2 * self.PI *  self.EPSILON_0 * self.epsilon_r)
        else: #L
            keisu = (self.MU_0 * self.mu_r)/(2 * self.PI)

        if Z0P1L2!=0: ZPL1=simplify(ZPL*keisu)

        return ZPL1


# end of Lines class
