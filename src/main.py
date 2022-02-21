



from math import acos, asin, cos, degrees, sqrt
import numpy as np

from neurovec3D import NeuroVector3D

def extract(x, y, z):
    ro = sqrt(x*x+y*y+z*z)

    if ro == 0:
        return [0, 0, 0]

    phi   = asin(z / ro)
    theta = asin(y / (ro * cos(phi)))

    return [theta, phi, ro]

v1 = np.array([1, 2, 3])
v2 = np.array([5, 4, 6])
v3 = v1 * 5

nv1 = NeuroVector3D.fromCartesianVector(*v1, 3600)
nv2 = NeuroVector3D.fromCartesianVector(*v2, 3600)


nv3 = nv1 * 5


a = NeuroVector3D.extractPolarParameters(nv3)
b = np.array(extract(*v3))

res = np.array(a)-np.array(b)

extv3 = np.array(NeuroVector3D.extractCartesianParameters(nv3))
dot = v3.dot(extv3)
lin = np.linalg.norm(v3) * np.linalg.norm(extv3)
ang = acos(dot / lin)

print(degrees(ang))

res[0] = degrees(res[0])
res[1] = degrees(res[1])

print(extv3)
print(v3)

print(res)


