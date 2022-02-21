


import numpy as np


a = np.random.random((5,5))

m = a.max()

xs, ys = np.where(a==m)
x, y = xs[0], ys[0]


print(a[x, y], m)