import numpy as np
from neurovec3D import NeuroVector3D


def reachedActionPotential(a: NeuroVector3D) -> bool:
    return ((a.getMS() - a.bias) > 0.1).any()

def doAND(a, b):
    # excitatory
    return NeuroVector3D.fromMS(reachedActionPotential(b) * (a.getMS() - a.bias))

def doNOT(a):
    b = np.ones(a.getMS().shape)
    # inhibitory
    return NeuroVector3D.fromMS((not reachedActionPotential(a)) * b)

def doNAND(a, b):
    return doNOT(doAND(a, b))

def doOR(a, b):
    return doNAND(doNOT(a), doNOT(b))

def doXOR(a, b):
    return doAND(doOR(a, b), doNAND(a, b))

def sr_latch(d, n):
    c = NeuroVector3D.fromMS(np.zeros(d.getMS().shape))
    a = doNOT(doOR(d, n)) # 1
    n = doNOT(doOR(a, c)) # 0

    return n
"""
a = NeuroVector3D.fromCartesianVector(5, 3, 2, 5)
b = NeuroVector3D.fromCartesianVector(*np.random.random(3), 5)
c = NeuroVector3D.fromMS(np.zeros(a.getMS().shape))
r = NeuroVector3D.fromMS(np.zeros(a.getMS().shape))
d = NeuroVector3D.fromMS(np.ones(a.getMS().shape))


c = sr_latch(doNOT(a), r, c)
print(c.getMS())
c = sr_latch(doNOT(a), r, c)
print(c.getMS())
c = sr_latch(doNOT(a), r, c)
print(c.getMS())
c = sr_latch(doNOT(r), r, c)
print(c.getMS())
c = sr_latch(doNOT(a), r, c)
print(c.getMS())
c = sr_latch(doNOT(a), r, c)
print(c.getMS())
"""