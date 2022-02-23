from math import cos, degrees, sin
from random import random
from tkinter import N
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('..')

from src.neurovec2D import NeuroVector2D
from src.neurovec3D import NeuroVector3D

np.random.seed(2)

av1 = np.random.random(3)
av2 = np.random.random(3)

a=NeuroVector3D(4, 0, 0, 1000)
b=NeuroVector3D(2, 0, 0, 1000)

c=NeuroVector3D(6, -np.pi, -np.pi, 1000)

print(c.extractCartesianParameters())


print(a.extractCartesianParameters())
print(b.extractCartesianParameters())
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
