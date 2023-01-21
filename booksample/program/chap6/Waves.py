# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 18:27:26 2016

@author: abemasayuki
"""
import numpy as np

def SquareWave(PulseHeight, FallEdgeTime, PeriodTime, dt):
    SlopePixel=2 #needs adjustment

    PulseSlope=PulseHeight/np.float(SlopePixel)
    PeriodInt=int(PeriodTime/dt)
    FallEdgeInt=int(FallEdgeTime/dt)
    SW=np.zeros(PeriodInt)

    for i in range (PeriodInt):
        if i==0:
            SW[i] = 0.0
        elif i<SlopePixel:
            SW[i] = PulseSlope * np.float(i)
        elif i>=SlopePixel and i<=(FallEdgeInt-SlopePixel):
            SW[i] = PulseHeight
        elif i>(FallEdgeInt-SlopePixel) and i<=FallEdgeInt:
            SW[i] = (FallEdgeInt*PulseSlope-PulseSlope*np.float(i))
        else:
            SW[i]=0.0

    return SW
