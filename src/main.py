import numpy as np

from math import atan2, sqrt

from neurovec2D import NeuroVector2D

def thro(x, y):
    theta = atan2(y, x)
    ro = sqrt(x*x+y*y)
    return theta, ro

vec = np.array([10, 20])
vec2= np.array([5, 11])

t,r=thro(*vec)
t1,r1=thro(*vec2)

nv = NeuroVector2D(r, t,   3600)
nv2= NeuroVector2D(r1, t1, 3600)

nv3 = nv2 - nv


print(nv3.toVec())
#print(nv3.toVec())