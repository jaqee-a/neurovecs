from math import asin, sqrt, cos
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
import sys
import matplotlib.colors as colors
sys.path.append('..')

from src.neurovec3D import NeuroVector3D


def extract(x, y, z):
    ro = sqrt(x*x+y*y+z*z)

    if ro == 0:
        return [0, 0, 0]

    phi   = asin(z / ro)
    theta = asin(y / (ro * cos(phi)))

    return [theta, phi, ro]
    
N=100

v1 = np.array([1, 2, 3])
nv1= NeuroVector3D.fromCartesianVector(*v1, N)

ms = NeuroVector3D.getMS(nv1)

# Make data.
X = np.linspace(-np.pi, np.pi, N, endpoint=True)
Y = np.linspace(-np.pi, np.pi, N, endpoint=True)
# X, Y = np.meshgrid(X, Y)

Z = ms

print(*extract(*v1))

fig, ax = plt.subplots(1, 1)

#pcm = ax.pcolor(X, Y, Z,
#                   norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),
#                   cmap='PuBu_r', shading='nearest')
#fig.colorbar(pcm, ax=ax, extend='max')

pcm = ax.pcolor(X, Y, Z, cmap='PuBu_r', shading='nearest')
fig.colorbar(pcm, ax=ax, extend='max')

plt.show()
exit()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(ms.min(), ms.max())
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()