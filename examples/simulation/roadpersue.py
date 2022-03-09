



from math import acos, degrees, sqrt
import glm
from neurovec3D import NeuroVector3D

from simulation.simulation import Simulation

class RoadPursue(Simulation):

    def __init__(self, resolution: int, type_: str) -> None:
        super().__init__(resolution, type_)

        self.dt = glm.vec3(0)
        self.D  = 10
        self.H  = 5

    def getReferenceVectors(self):
        rp  = self.prey - self.pred

        up  = glm.vec3(0, 1, 0) * self.H

        h   = self.prey + up
        dh  = glm.vec3(0, h.y - self.pred.y, 0)

        d   = self.pred + dh - h

        d2  = sqrt(self.D**2 - self.H ** 2)
        
        # d1  = d * ((glm.length(d) - d2) / glm.length(d))

        return dh, d, d2, rp#dh - d1, rp
    
    def simulationOver(self):
        return self.iteration > 50000

    def run(self):
        super().run()

        if self.simulationOver(): return False

        # Can be found in the parent class also.
        self.updatePreyPosition()

        # Get the needed reference vectors
        dh, d, d2, _ = self.getReferenceVectors()

        n_dh    = NeuroVector3D.fromCartesianVector(*dh , self.resolution)
        n_d     = NeuroVector3D.fromCartesianVector(*d, self.resolution)
        _, _, r = NeuroVector3D.extractPolarParameters(n_d)

        n_d1    = n_d * float((r - d2) / r)

        dt      = n_dh - n_d1

        dt_cart = glm.vec3(*NeuroVector3D.extractCartesianParameters(dt))

        self.pred += dt_cart

        # Calculate the error and speed
        if self.iteration > 1:
            self.errors.append(self.getError())
            self.speed .append(glm.length(dt_cart))

        return True


    def getError(self):
        *_,rp = self.getReferenceVectors()
        dis  = abs(self.D - glm.length(rp))

        return dis