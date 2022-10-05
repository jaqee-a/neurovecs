import numpy as np
from user import User

from neurovec3D import NeuroVector3D

import core.components.transform
import core.components.camera
import core.components.cMesh
import core.components.mesh
import core.application
import core.time

import glm

class Drone :

    colors = [(0,255,0,1), (255,0,0,1), (0,0,255,1), (255,255,0,1), (151,13,117,1), (0,255,255,1), (255,0,255,1), (151,13,117,1), (20,20,100,1), (0,20,100,1)]
    i = 0

    transmission_power  = 20 # db
    bandwidth           = 100 * 10**6 #Hz
    theta               = 42.44 #degrees
    capacity            = 30
    resolution = 10
    initPosition1 = [300, 40, 300]
    initPosition2 = [0, 10, 200]

    def __init__ (self, app, droneMesh,  position = [300, 40, 300]) :
        
        self.m_app = app

        self.color           = Drone.colors[Drone.i % 10]
        self.n_users         = 0
        self.connected_users = []
        
        self.position  = glm.vec3(position) #meter
        self.obj       = self.generateFromMesh(droneMesh, self.position, app)
       
        Drone.i += 1
        self.lastStop = glm.vec3(0, 15, 300)
        

    def generateFromMesh(self, mesh: core.components.mesh.Mesh, position, app):

        obj = app.m_ActiveScene.makeEntity()
        obj.linkComponent(mesh)
        obj.addComponent(core.components.transform.Transform, *position, *([0]*3))

        return obj

    def destroy(self):
        self.m_app.m_ActiveScene.m_Registry.removeEntity(self.obj)


    def force(self, users, drones, non_con, obstacles) :

        #Attracton force with the users 
        init = glm.vec3(0)
        F1   = NeuroVector3D.fromCartesianVector(*init, self.resolution)

        for user in users :
            if user.isConnected == None :
                v   = user.position - self.position
                n_v = NeuroVector3D.fromCartesianVector(*v, self.resolution)
                l   = NeuroVector3D.extractPolarParameters(n_v)[2]
                NeuroVector3D.normalize(n_v)
                F1 += n_v * float((1 - 1 / l) * (1 / non_con))
        
        #Repulsion force with other drones
        F2 = NeuroVector3D.fromCartesianVector(*init, self.resolution)

        for drone in drones :
            if self.position != drone.position :
                v   = self.position - drone.position
                n_v = NeuroVector3D.fromCartesianVector(*v, self.resolution)
                l   = NeuroVector3D.extractPolarParameters(n_v)[2]
                NeuroVector3D.normalize(n_v)
                F2 += n_v * float((1 / l ) * non_con)

        #Repulsion force with the obstacles
        F3 = NeuroVector3D.fromCartesianVector(*init, self.resolution)

        for obstacle in obstacles :
            if obstacle.type == 'y' :
                obstacle.position.y = self.position.y
                v   = self.position - obstacle.position
                n_v = NeuroVector3D.fromCartesianVector(*v, self.resolution)
                l   = (NeuroVector3D.extractPolarParameters(n_v)[2] - 16)
                NeuroVector3D.normalize(n_v)
                F3 += n_v * float(1 / (l**2))
            
        
        #Repulsion force with the ground
        ground = glm.vec3(0, 1, 0)
        gr     = NeuroVector3D.fromCartesianVector(*ground, self.resolution)
        heigth = glm.vec3(0, self.position.y, 0)
        h      = NeuroVector3D.fromCartesianVector(*heigth, self.resolution)
        l_h    = NeuroVector3D.extractPolarParameters(h)[2]

        F4     = gr *  float(1 / (l_h ** 2) * len(users))

        n_F = F1 + F2 + F3 + F4
        F = NeuroVector3D.extractCartesianParameters(n_F)

        return F



    def EnergyConsumption(self, v) :

        p0 = 577.3  # Watt   ---> Blade profile power
        pi = 793.0  # Watt   ---> induced power
        Utip = 200  # m/s    ---> tip speed of the rotor blade
        v0 = 7.21   # m/s    ---> the mean rotor induced velocity in hover
        d0 = 0.3    #        ---> fusilage drag ratio
        rho = 1.225 # kg/m3  ---> Air density
        s = 0.05    #        ---> rotor solidity
        A = 0.79    # m2     ---> rotor disk area

        p = p0 * (1 + (3* v**2 / Utip**2)) + pi * (np.sqrt(1+(v**4/4*v0**4))-(v**2/2*v0**2))**(1/2) + 1/2*d0*rho*s*A*v**3

        return p * 10**-3