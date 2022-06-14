from math import sqrt
import glm
from neurovec3D import NeuroVector3D
from core.primitives import cube, cube2

from simulation.simulation import Simulation

class RoadPursue(Simulation):

    def __init__(self, resolution: int, type_: str, app) -> None:
        super().__init__(resolution, type_)

        self.dt = glm.vec3(0)
        self.D  = 5
        self.H  = 5
        self.tresh = 0.5

        self.ground = cube(app.m_ActiveScene, (25, 0, 25), (.3, .3, .3, 1), (30, 1, 300))
        self.uproad = cube2(app.m_ActiveScene, (25, 2.5, 25), (.4, .4, .4, 1), (30, 4, 30))
        #self.base   = cube(app.m_ActiveScene, (37.5, 5, -122.5), (.3, .3, .3, 1), (5, 10, 5))

        self.pred = glm.vec3(10, 5, -122.5)
        self.prey = glm.vec3(10, 0.7, -100)


    def getReferenceVectors(self):
        rp  = self.prey - self.pred

        up  = glm.vec3(0, 1, 0) * self.H

        h   = self.prey + up
        """
        dh  = glm.vec3(0, h.y - self.pred.y, 0)

        d   = self.pred + dh - h

        d2  = sqrt(self.D**2 - self.H ** 2)"""
        

        return rp, h
    
    def simulationOver(self):
        return self.iteration > 50000

    def sigmoide(self, x) :
        
        return 1 / (1 + 2.72**(-100*x))

    def velocity(self, v, tresh) :

        return float(v * self.sigmoide(v) - (v - tresh) * self.sigmoide(v - tresh))

    def preyPosition(self, position):
        vel = 0.05

        if 10 < position.z < 17 :
            position.y += (4*vel / 6)
            position.z += vel
        elif 35 < position.z < 40 :
            position.y -= (4*vel / 6)
            position.z += vel
        elif position.z > 50:
            position.z += 0
        else :
            position.z += 0.1

        return position
            

    def run(self):
        super().run()

        if self.simulationOver(): return False

        # Can be found in the parent class also.
        self.prey = self.preyPosition(self.prey)
        # Get the needed reference vectors
        rp, h = self.getReferenceVectors()

        n_rp    = NeuroVector3D.fromCartesianVector(*rp , self.resolution)
        n_h     = NeuroVector3D.fromCartesianVector(*h, self.resolution)
        _, _, r = NeuroVector3D.extractPolarParameters(n_rp)

        n_rp    = n_rp * float(1 - self.D / r)
        
        #n_rp = n_rp * 0.6
        #n_h  = n_h * 0.4
        dt   = n_rp

        """_, _, r = NeuroVector3D.extractPolarParameters(dt)

        vel = self.velocity(r, self.tresh)
        NeuroVector3D.normalize(dt)"""

        dt_cart = glm.vec3(*NeuroVector3D.extractCartesianParameters(dt))

        self.pred += dt_cart

        # Calculate the error and speed
        if self.iteration > 1:
            self.errors.append(self.getError())
            self.speed .append(glm.length(dt_cart))
            print(glm.length(dt_cart))

        return True


    def getError(self):
        *_,rp = self.getReferenceVectors()
        dis  = abs(self.D - glm.length(rp))

        return dis