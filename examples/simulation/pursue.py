import glm
import numpy as np
from neurovec3D import NeuroVector3D
import matplotlib.pyplot as plt

from simulation.simulation import Simulation

class Pursue(Simulation):

    def __init__(self, resolution: int, type_: str) -> None:
        super().__init__(resolution, type_)

        self.dt = glm.vec3(0)
        self.D  = 5

        self.prey = glm.vec3(0,0,15)

        self.speed_p = []
        self.distance = []

    def getReferenceVectors(self):
        rp  = self.prey - self.pred

        return rp
    
    def simulationOver(self):
        return  self.iteration > 700
         
    def run(self):
        super().run()

        if self.simulationOver(): return False

        # Can be found in the parent class also.
        self.updatePreyPosition()
        

        # Get the needed reference vectors
        rp  = self.getReferenceVectors()

        # Create Neuron Vectors
        n_rp  = NeuroVector3D.fromCartesianVector(*rp , self.resolution)

        dist  = NeuroVector3D.extractPolarParameters(n_rp)[2]

        dt    = n_rp * float( 1 - (self.D / dist))

        # Turn the neuron vector into a cartesian vector 
        dt_cart = glm.vec3(*NeuroVector3D.extractCartesianParameters(dt))

        self.pred += dt_cart

        # Calculate the error and speed
        if self.iteration > 1:
            self.errors.append(self.getError())
            self.speed .append(glm.length(dt_cart))
           

            self.distance.append(glm.length(self.prey - self.pred))

        return True


    def getError(self):
        rp  = self.getReferenceVectors()
        dis = abs(self.D - glm.length(rp))

        return dis