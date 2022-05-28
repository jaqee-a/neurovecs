import numpy as np
import glm
from neurovec3D import NeuroVector3D

from simulation.nomovesimulation import NoMoveSimulation

class UavSimulation(NoMoveSimulation):

    def __init__(self, resolution: int) -> None:
        super().__init__(resolution)
        
    def getReferenceVectors(self):
        pass
    
    def simulationOver(self):
        return self.iteration > 50000

    def run(self):
        super().run()

        return True
