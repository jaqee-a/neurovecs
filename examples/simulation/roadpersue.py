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
        
        dh = n_rp_d + n_h
        a = 1 / (r_hp - self.H)
 
        dt = (n_rp_d * float(1 - a)) + (dh * float(a))
        
        
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