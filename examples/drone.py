import numpy as np
from user import User

import core.components.transform
import core.components.camera
import core.components.cMesh
import core.components.mesh
import core.application
import core.time

import glm

class Drone :

    colors = [(255,0,0,1), (0,255,0,1), (0,0,255,1), (255,255,0,1), (0,255,255,.1), (255,0,255,.1), (50,200,0,.1), (50,0,200,.1), (20,20,100,.1), (0,20,100,.1)]
    i = 0

    transmission_power  = 20 # db
    bandwidth           = 40 * 10**6 #Hz
    theta               = 42.44 #degrees
    capacity            = 30

    def __init__ (self, app, droneMesh, coneMesh) :

        self.color           = Drone.colors[Drone.i % 10]
        self.n_users         = 0
        self.connected_users = []
        
        self.position  = glm.vec3(0, 20, 0) #meter
        self.obj       = self.generateFromMesh(droneMesh, self.position, app).getComponent(core.components.transform.Transform)
        self.coneObj   = self.generateFromMesh(coneMesh, self.position-glm.vec3(0, self.position.y, 0), app).getComponent(core.components.transform.Transform)
        
        Drone.i += 1

        #cone(app.m_ActiveScene, (25, 0, 25), 8, [0, 0, 1, .1], [5, 20, 5])


    def generateFromMesh(self, mesh: core.components.mesh.Mesh, position, app):

        obj = app.m_ActiveScene.makeEntity()
        obj.linkComponent(mesh)
        obj.addComponent(core.components.transform.Transform, *position, *([0]*3))

        return obj

    def r(self) :
        
        snr = 15
        r = 0
        while snr >= 15 :
            r += 1
            snr = User.SNR(self, r)[0]
        return r


    def force(self, users, drones, non_con) :

        #Attracton force with the users 
        F1 = glm.vec3(0)

        for user in users :
            if user.isConnected == None :
                v = user.position - self.position
                F1 += glm.normalize(v) * 1 / (glm.length(v) * (non_con / len(drones)))
        
        #Repulsion force with other drones
        F2 = glm.vec3(0)

        for drone in drones :
            if self.position != drone.position :
                v = self.position - drone.position
                F2 += glm.normalize(v) * 1 / (glm.length(v) * len(drones))

        #Repulsion force with the obstacles
        F3 = glm.vec3(0)

        """for ob in obstacles :
            v = ((self.position) + glm.vec3(50, 0, 50)) - ob[0]
            F3 += glm.normalize(v) * 1 / (glm.length(v)**2)"""
        
        #Repulsion force with the ground
        F4 = glm.vec3(0, 1, 0) * 1 / (self.position.y**2)

        F = F1 + F2 + F3 + F4

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