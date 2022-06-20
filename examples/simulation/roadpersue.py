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
        self.H  = 8
        self.tresh = 0.2

        """self.ground = cube(app.m_ActiveScene, (25, 0, 25), (.3, .3, .3, 1), (30, 1, 300))
        self.uproad = cube2(app.m_ActiveScene, (25, 2.5, 25), (.4, .4, .4, 1), (30, 4, 30))
        self.base   = cube(app.m_ActiveScene, (37.5, 5, -122.5), (.3, .3, .3, 1), (5, 10, 5))"""

        self.pred = glm.vec3(25, 5, -32.5)
        self.prey = glm.vec3(25, 0.7, -10)

        self.ph = glm.vec3(0, 5, 0)


    def getReferenceVectors(self):
        
        rp  = self.prey - self.pred

        up  = glm.vec3(0, 1, 0) * self.H

        h   = self.prey + up

        self.updateHeight(self.pred)
        
        """
        dh  = glm.vec3(0, h.y - self.pred.y, 0)

        d   = self.pred + dh - h

        d2  = sqrt(self.D**2 - self.H ** 2)"""
        
        return rp, self.ph
    
    def simulationOver(self):
        return self.iteration > 50000

    def sigmoide(self, x) :
        
        return 1 / (1 + 2.72**(-100*x))

    def velocity(self, v, tresh) :

        return float(v * self.sigmoide(v) - (v - tresh) * self.sigmoide(v - tresh))

    def updatePreyPosition(self, position):
        vel = 0.05

        if 10 < position.z < 16 :
            position.y += (4*vel / 6)
            position.z += vel
        elif 34 < position.z < 40 :
            position.y -= (4*vel / 6)
            position.z += vel
        elif position.z > 50:
            position.z += 0
        else :
            position.z += 0.1

        return position
    
    def updateHeight(self, position) :

        if 10 < position.z < 16 :
            self.ph.y -= (4*0.05 / 6)
            
        elif 34 < position.z < 40 :
            self.ph.y += (4*0.05 / 6)
            

    def run(self):
        super().run()

        if self.simulationOver(): return False
     
        self.prey = self.updatePreyPosition(self.prey)
        
        # Get the needed reference vectors
        rp, h = self.getReferenceVectors()

        n_rp    = NeuroVector3D.fromCartesianVector(*rp , self.resolution)
        
        n_h     = NeuroVector3D.fromCartesianVector(*h, self.resolution)
        n_hp     = NeuroVector3D.fromCartesianVector(*self.ph, self.resolution)
        _, _, r_rp = NeuroVector3D.extractPolarParameters(n_rp)
        _, _, r_hp = NeuroVector3D.extractPolarParameters(n_hp)
          
       
        n_rp_d = n_rp * float(1 - self.D / r_rp)
        r_rp_d = NeuroVector3D.extractPolarParameters(n_rp_d)[2]

        h1 = r_rp_d * r_hp / r_rp
        h2 = r_hp - h1
        h = 0
        if h2 < self.H : h = self.H - h2 
    
        vh = glm.vec3(0, h, 0)
        n_vh = NeuroVector3D.fromCartesianVector(*vh, self.resolution)

        dt = n_rp_d + n_vh
        """_, _, r = NeuroVector3D.extractPolarParameters(dt)
        
        vel = self.velocity(r, self.tresh)
        NeuroVector3D.normalize(dt)"""

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