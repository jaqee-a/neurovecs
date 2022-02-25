import numpy as np
from neurovec3D import NeuroVector3D
from neurovec2D import NeuroVector2D


a = np.array([1, 2])
b = np.array([3, 2])


print(a+(-b))

na = NeuroVector2D.fromCartesianVector(*a, 360)
nb = NeuroVector2D.fromCartesianVector(*b, 360)

print(NeuroVector2D.extractCartesianParameters(na-nb))