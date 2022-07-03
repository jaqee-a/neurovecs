from math import sqrt
import glm
from neurovec3D import NeuroVector3D
from core.primitives import cube, cube2

from simulation.simulation import Simulation
import matplotlib.pyplot as plt

import numpy as np

class RoadPursue(Simulation):

    def __init__(self, resolution: int, type_: str, app) -> None:
        super().__init__(resolution, type_)

        self.dt = glm.vec3(0)
        self.D  = 10
        self.H  = 6
        self.tresh = 0.2

        """self.ground = cube(app.m_ActiveScene, (25, 0, 25), (.3, .3, .3, 1), (30, 1, 300))
        self.uproad = cube2(app.m_ActiveScene, (25, 2.5, 25), (.4, .4, .4, 1), (30, 4, 30))
        self.base   = cube(app.m_ActiveScene, (37.5, 5, -122.5), (.3, .3, .3, 1), (5, 10, 5))"""

        self.pred = glm.vec3(25, 7, -10.5)
        self.prey = glm.vec3(25, 0.7, -10)

        self.ph = glm.vec3(0, 0, 0)

        self.speed_t = []
        self.vel = 0.1

        self.distance = []

        self.up_vector = glm.normalize(glm.vec3(0,4,6))
        self.down_vector = glm.normalize(glm.vec3(0,-4,6))


    def getReferenceVectors(self, lprey):
        
        rp  = self.prey - self.pred
        self.updateHeight(self.pred)
        
        return rp, self.ph
    
    def simulationOver(self):

        return self.iteration > 50000
          

    def updatePreyPosition(self, position):

        if 10 < position.z < 16 :
            position += self.up_vector * self.vel
            self.vel -= 0.0005
        
        elif 16 <= position.z <= 34 :
            position.z += self.vel

        elif 34 < position.z < 40 :
            position += self.down_vector * self.vel
            self.vel += 0.0005

        elif position.z > 50 :
            self.iteration = 5000000

            #a = [i for i in range(len(self.speed_p))]
            b = [i for i in range(len(self.distance))]
            #plt.plot(a, self.speed_p, label = "Target")
            plt.plot(b, self.distance)
            plt.xlabel("Time (a.u.)", fontsize = "18")
            plt.ylabel("Distance (a.u.)", fontsize = "18")
            plt.ylim(5, 15)

            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(fontsize = "18")

            plt.show()
    
            """a = [i for i in range(len(self.speed_t))]

            fig, axs = plt.subplots(2)
            #fig.suptitle('Vertically stacked subplots')
            axs[0].plot(a, self.speed_t)
            axs[1].plot(a, self.speed, 'tab:orange')
            axs[0].set_title("Target")
            axs[1].set_title("Tracker")
            
            axs[0].set(ylabel="Speed (a.u.)", ylim = [.01, .12])
            axs[1].set(xlabel="Time (a.u.)", ylabel="Speed (a.u.)", ylim = [.02, .12])

            plt.show()"""
        else :
            position.z += self.vel

        return position
    
    def updateHeight(self, position) :

        self.ph.y = self.pred.y
        if 10 < position.z < 16 :
            y = (position.z - 10) * 4 / 6
            self.ph.y -= y
        
        elif 34 < position.z < 40 :
            y = (40 - position.z) * 4 / 6
            self.ph.y += y
        

    def run(self):
        super().run()

        if self.simulationOver(): return False
        
        lastPrey = glm.vec3(self.prey)
        self.prey = self.updatePreyPosition(self.prey)
        
        # Get the needed reference vectors
        rp, h = self.getReferenceVectors(lastPrey)

        n_rp    = NeuroVector3D.fromCartesianVector(*rp , self.resolution)
        n_hp    = NeuroVector3D.fromCartesianVector(*h, self.resolution)
        n_h     = NeuroVector3D.fromCartesianVector(*glm.vec3(0, self.H, 0), self.resolution)

        _, _, r_rp = NeuroVector3D.extractPolarParameters(n_rp)
        _, _, r_hp = NeuroVector3D.extractPolarParameters(n_hp)
          
       
        n_rp_d = n_rp * float(1 - self.D / r_rp)
        r_rp_d = NeuroVector3D.extractPolarParameters(n_rp_d)[2]

        
        dh = n_rp_d + n_h
        a = 1 / (r_hp - self.H)
 
        dt = (n_rp_d * float(1 - a)) + (dh * float(a))
        """h1 = r_rp_d * r_hp / r_rp
        h2 = r_hp - h1
        h = 0
        if h2 < self.H : h = self.H - h2 
    
        vh = glm.vec3(0, h, 0)
        n_vh = NeuroVector3D.fromCartesianVector(*vh, self.resolution)

        dt = n_rp_d + n_vh
        _, _, r = NeuroVector3D.extractPolarParameters(dt)"""
        
        
        #NeuroVector3D.normalize(dt)

        dt_cart = glm.vec3(*NeuroVector3D.extractCartesianParameters(dt))

        self.pred += dt_cart

        # Calculate the error and speed
        if self.iteration > 1:
            self.errors.append(self.getError())
            self.speed.append(glm.length(dt_cart))
            self.speed_t.append(glm.length(lastPrey - self.prey))
            
            self.distance.append(self.ph.y)


        return True


    def getError(self):
        rp = self.getReferenceVectors(glm.vec3(0))[0]
        dis  = abs(self.D - glm.length(rp))

        return dis