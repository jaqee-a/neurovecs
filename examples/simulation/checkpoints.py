import numpy as np
import glm
from neurovec3D import NeuroVector3D
from logic import *

from simulation.simulation import Simulation

class Checkpoint(Simulation):

    def __init__(self, resolution: int, type_: str) -> None:
        super().__init__(resolution, type_)


        self.prey = [glm.vec3(0, 0, 30), glm.vec3(-20, 0, 20), glm.vec3(20, 0, 20)]
        self.other= [[] for _ in range(len(self.prey))]
        self.dt = glm.vec3(0)
        self.D  = 5

        self.memory_signals = [NeuroVector3D.fromMS(np.zeros((self.resolution, self.resolution))) for _ in range(len(self.prey))]

    def getReferenceVectors(self):
        rp  = [cp - self.pred for cp in self.prey]

        return rp
    
    def simulationOver(self):
        return self.iteration > 50000

    def run(self):
        super().run()

        if self.simulationOver(): return False

        # Get the needed reference vectors
        rp  = self.getReferenceVectors()

        # Create Neuron Vectors
        n_rp  = []
        for i in range(len(rp)):
            n_rp.append(NeuroVector3D.fromCartesianVector(*rp[i] , self.resolution))


        v = doAND(n_rp[0], doNOT(self.memory_signals[0]))
        #print(n_rp[0].getMS() == v.getMS())
        self.memory_signals[0] = sr_latch(doNOT(v), self.memory_signals[0])
        res = v
        
        for i in range(len(n_rp)-1):
            index = i + 1
            v = doAND(n_rp[index], doNOT(self.memory_signals[index]))
            self.memory_signals[index] = sr_latch(doNOT(v), self.memory_signals[index])
            vv = doAND(v, doNOT(res))
            res = res + vv


        """
        Movement Logic
        
        """

        res.normalize()

        dt_cart = glm.vec3(*NeuroVector3D.extractCartesianParameters(res * 0.3))

        # dt_cart = glm.vec3(*NeuroVector3D.extractCartesianParameters(dt))

        self.pred += dt_cart
        if self.iteration > 1:
            for i in range(len(n_rp)):
                self.other[i] = n_rp[i].getMS().sum(axis=1)


        return True


    """
    def getError(self):
        rp  = self.getReferenceVectors()
        dis = abs(self.D - glm.length(rp))

        return dis
    """