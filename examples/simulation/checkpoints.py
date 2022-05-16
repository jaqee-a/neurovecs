import numpy as np
import glm
from neurovec3D import NeuroVector3D

from simulation.simulation import Simulation

class Checkpoint(Simulation):

    def __init__(self, resolution: int, type_: str) -> None:
        super().__init__(resolution, type_)


        self.prey = [glm.vec3(0, 0, 30), glm.vec3(-20, 0, 20), glm.vec3(20, 0, 20)]
        self.other= [[] for _ in range(len(self.prey))]
        self.dt = glm.vec3(0)
        self.D  = 5

        self.memory_signals = [np.ones((self.resolution, self.resolution)) for _ in range(len(self.prey))]

    def getReferenceVectors(self):
        rp  = [cp - self.pred for cp in self.prey]

        return rp
    
    def simulationOver(self):
        return self.iteration > 50000

    def doOR(self, pv1: np.ndarray, pv2: np.ndarray):
        cp = pv1.copy()
        cp[cp < 0.1] = pv2[cp < 0.1]
        return cp

    def doAND(self, pv1: np.ndarray, pv2: np.ndarray):
        cp = pv2.copy()
        cp[pv1 < 0.1] = 0
        return cp

    def reachedActionPotential(self, pv1: np.ndarray) -> bool:
        return (pv1 > 0.1).any()

    def run(self):
        super().run()

        if self.simulationOver(): return False

        # Get the needed reference vectors
        rp  = self.getReferenceVectors()

        # Create Neuron Vectors
        n_rp  = []
        for i in range(len(rp)):
            n_rp.append(NeuroVector3D.fromCartesianVector(*rp[i] , self.resolution))


        """
        Movement Logic
        
        """

        sum_force = self.doAND(self.memory_signals[0], n_rp[0].getMS())
        self.memory_signals[0] *= self.reachedActionPotential(sum_force - 50)#self.doAND(sum_force - 50, self.memory_signals[0])

        for i in range(len(n_rp) - 1):
            local_force = self.doAND(self.memory_signals[i + 1], n_rp[i + 1].getMS())
            self.memory_signals[i + 1] *= self.reachedActionPotential(local_force - 50)

            #local_force = self.doAND(np.logical_not(self.memory_signals[i]) * 1.0, local_force - 50)

            sum_force = self.doOR(sum_force, local_force)

        print(sum_force)

        dt = NeuroVector3D.fromMS(sum_force * 0.001, 0)

        dt_cart = glm.vec3(*NeuroVector3D.extractCartesianParameters(dt))

        self.pred += dt_cart
        
        if self.iteration > 1:
            for i in range(len(n_rp)):
                self.other[i] = n_rp[i].getMS().sum(axis=1)


        return True


        dist  = NeuroVector3D.extractPolarParameters(n_rp)[2]


    """
    def getError(self):
        rp  = self.getReferenceVectors()
        dis = abs(self.D - glm.length(rp))

        return dis
    """