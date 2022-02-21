



from math import sqrt
import numpy as np

from neurovec3D import NeuroVector3D


v1 = np.array([1, 2, 3])
v2 = np.array([5, 4, 6])
v3 = v1 + v2

nv1 = NeuroVector3D.fromCartesianVector(*v1, 3600)
nv2 = NeuroVector3D.fromCartesianVector(*v2, 3600)


nv3 = nv1 + nv2


print(NeuroVector3D.extractCartesianParameters(nv3))
