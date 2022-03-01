from math import acos, degrees
import glm
from neurovec3D import NeuroVector3D

from simulation.simulation import Simulation

class FixedPoint(Simulation):

    def __init__(self, resolution: int, type_: str) -> None:
        super().__init__(resolution, type_)

        self._lambda = 0

    def getReferenceVectors(self):
        rfp = self.pred - self.point
        rp  = self.prey - self.pred

        return rfp, rp
        
    def run(self):
        super().run()

        # distance < .3, can be found in the parent class since its a shared function
        if self.simulationOver(): return False

        # Can be found in the parent class also.
        self.updatePreyPosition()

        # Get the needed reference vectors
        rfp, rp = self.getReferenceVectors()

        # Create Neuron Vectors
        n_rfp = NeuroVector3D.fromCartesianVector(*rfp, self.resolution)
        n_rp  = NeuroVector3D.fromCartesianVector(*rp , self.resolution)

        dt    = n_rp * self._lambda + n_rfp * (self._lambda - 1)

        # Turn the neuron vector into a cartesian vector 
        dt_cart = glm.vec3(*NeuroVector3D.extractCartesianParameters(dt))

        self.pred += dt_cart

        # update lambda
        self._lambda += self.alpha * ( 1 - self._lambda )

        # Calculate the error and speed
        if self.iteration > 1:
            self.errors.append(self.getError())
            self.speed .append(glm.length(dt_cart))

        return True


    def getError(self):
        rfp, rp = self.getReferenceVectors()
        v12     = glm.length(rfp) * glm.length(rp)
        cosa    = glm.dot(rfp, rp) / v12

        # Sometimes cos(a) gets over 1 by epsilon
        # and its a something that shouldn't happen
        # but we can fix it by setting cos(a) back to 1
        if cosa > 1: cosa = 1
        #-----------------------------------------------
        
        a       = degrees(acos(cosa))

        return a