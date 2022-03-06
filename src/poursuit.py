import numpy as np
import matplotlib.pyplot as plt
from pygame import Vector3
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from neurovec3D import NeuroVector3D




class poursuite:
    
    def __init__(self, res):
        
        self.res = res
       
        self.dr = Vector3(100, 0, 0)
        self.dr_cible = Vector3(0, 0, 0)
        self.v = Vector3(0,10,10)
        self.dist = 50

        self.t = [self.dr]
        self.t_c = [self.dr_cible]

        self.iter = 0

    def update(self):
        
        ref = self.dr_cible - self.dr
        n_ref = NeuroVector3D.fromCartesianVector(ref.x, ref.y, ref.z, self.res)
        
        n_dt =  n_ref*float((1-self.dist/n_ref.extractPolarParameters()[2]))
        dt = Vector3(n_dt.extractCartesianParameters())

        self.dr = self.dr + dt
        
        if self.iter % 10 == 0 :
                axis = [Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1)]
                np.random.shuffle(axis)
                self.v = self.v.rotate(30, axis[0])
        
        self.dr_cible = self.dr_cible + self.v

        self.t.append(self.dr)
        self.t_c.append(self.dr_cible)
                       

    def draw(self, g1, g2):

        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(g1[0][0], g1[1][0], g1[2][0])
    
        ax.plot(g1[0], g1[1], g1[2], label='dr')
        ax.plot(g2[0], g2[1], g2[2], label='dr_cible')
        

        ax.legend()

        plt.show()

c = poursuite(10)

for _ in range(100):
   c.update()

x = [i[0] for i in c.t]
y = [i[1] for i in c.t]
z = [i[2] for i in c.t]

x1 = [i[0] for i in c.t_c]
y1 = [i[1] for i in c.t_c]
z1 = [i[2] for i in c.t_c]

c.draw([x,y,z], [x1,y1,z1])

