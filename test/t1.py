



from math import acos, atan2, cos, degrees, sin, sqrt
from random import random
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('..')

from src.neurovec2D import NeuroVector2D
from src.neurovec3D import NeuroVector3D

aa = np.array([1, 2, 3])

a = NeuroVector3D.fromCartesianVector(*aa, 16)

a = a * -2

print(a.extractCartesianParameters())

exit()
np.random.seed(2)

# av1 = np.random.random(3)
# av2 = np.random.random(3)

a = NeuroVector3D.fromCartesianVector(*np.array([0, 5, 0]), 5)

print(a.extractPolarParameters())
print(a.extractCartesianParameters())
exit()
b = NeuroVector3D.fromCartesianVector(*np.array([0, 0, 0]), 4)

azimuth   = np.linspace(-np.pi, np.pi, 4, endpoint=False)

na = a + b#NeuroVector3D.fromCartesianVector(*a, 4).extractCartesianParameters()

vv = NeuroVector3D.extractCartesianParameters(a)
phi, theta, rho = na.extractPolarParameters()

print(vv)

exit()
dot = np.array(vv).dot(np.array([0,5,0]))
v1 = np.linalg.norm(np.array(vv))*np.linalg.norm(np.array([0, 5, 0]))

print(degrees(acos(dot/v1)))

exit()

azimuth   = np.linspace(-np.pi, np.pi, 4, endpoint=True)
elevation = np.linspace(-np.pi/2, np.pi/2, 4, endpoint=True)

ones   = np.ones((4, 4))
phis   = (azimuth   * ones).T
thetas =  elevation * ones

__MS = rho * (cos(phi) * np.cos(phis) * np.cos(thetas - theta) + sin(phi) * np.sin(phis))

print(phis)
print()
print(thetas)
print()
print(__MS)
print()
print(theta)



exit()
__MS1 = (cos(0.9302740141154721) * np.cos(1.04719755) * np.cos(0.52359878 - 1.1071487177940904) + sin(0.9302740141154721) * np.sin(1.04719755))

__MS2 = (cos(0.9302740141154721) * np.cos(1.04719755) * np.cos(1.57079633 - 1.1071487177940904) + sin(0.9302740141154721) * np.sin(1.04719755))

print("MS", __MS1 , __MS2)

v1 = NeuroVector3D.fromCartesianVector(*a, 4)
v1a = v1.extractPolarParameters()
print(v1a)
# print(v1.extractCartesianParameters())
exit()
print(degrees(acos(a.dot(v1a) / (np.linalg.norm(a) * np.linalg.norm(v1a)))))
print(v1.extractCartesianParameters())
exit()

a=NeuroVector3D(6, np.pi/2, np.pi, 4)
b=NeuroVector3D(6, np.pi/2+np.pi, np.pi, 4)

c=a+b
print(np.round(c.extractCartesianParameters()))

print(np.round((b+a).extractCartesianParameters()))
print(np.round((b+a).extractPolarParameters()))

exit()
c=a+b
print(np.where(c.getMS() == c.getMS().max()))
print(c.extractCartesianParameters())
exit()

ms = a.getMS()
vs = ms.reshape(ms.shape[0]*ms.shape[1])
print(np.where(ms == ms.max()))

print(a.extractPolarParameters())
print(a.extractCartesianParameters())

print(a.extractCartesianParameters())
# print(b.extractCartesianParameters())
# print(c.extractCartesianParameters())
