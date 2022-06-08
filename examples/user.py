import random
import pygame
import numpy as np
import sys
import glm


sys.path.append('py-engine')

from core.primitives import cone, cube, line
import core.components.transform
import core.components.camera
import core.components.cMesh
import core.components.mesh
import core.application
import core.time



class User :

    def __init__(self, height, width, obs, app) -> None:
        
        self.height, self.width = height, width
        self.velocity    = random.uniform(1.25, 1.5) # m/s
        self.position    = glm.vec3(random.randint(5, 45), 1, random.randint(5, 45))

        self.userMesh    = self.makeUserMesh(app)
        self.obj         = self.generateFromMesh(self.userMesh, self.position, app).getComponent(core.components.transform.Transform)
        self.isConnected = None
        self.theta       = 0
        self.beta        = 0
        self.delta_theta = 0.3
        self.delta_t     = 200
        self.obs         = []
        """for ob in self.obs :
            if ob[0].z == 0 :
               self.obs.append(pygame.Rect(ob[0].x-int(ob[1][0]/2), ob[0].y-int(ob[1][1]/2), ob[1][0], ob[1][1]))
        """
        while self.isValid() == False :
              self.postion = pygame.Vector3(random.randint(0, 100), random.randint(0, 100), 0)
              self.obj.m_Position = self.position

              
    def makeUserMesh(self, app):

        user = cube(app.m_ActiveScene, (0, 0, 0), (.8, .3, .4, 1), (.3, 1, .3))
        user.m_isActive = False

        return user.getComponent(core.components.mesh.Mesh)
        

    def generateFromMesh(self, mesh: core.components.mesh.Mesh, position, app):

        obj = app.m_ActiveScene.makeEntity()
        obj.linkComponent(mesh)
        obj.addComponent(core.components.transform.Transform, *position, *([0]*3))

        return obj

    def isValid(self):

        for ob in self.obs :
            if ob.collidepoint(self.postion.x, self.position.z) == True :
                return False
                
        return True
    
    def randomWalk(self, iter, time) :

        
        #v = self.velocity * time / 1000
        v = .01
    
        if iter % self.delta_t == 0 :
           a = random.randint(0, 360)
           self.theta = a * np.pi / 180

        elif self.isValid() == False :
           self.theta += np.pi
        
        elif self.position.x < 5 or self.position.x > 45 or self.position.z < 5 or self.position.z > 45 :
            self.theta += np.pi

        self.beta = random.uniform(0,1)
        self.delta_theta = 0.3 - 0.6 * self.beta

        self.theta += self.delta_theta

        self.position.x += v * np.cos(self.theta) 
        self.position.z += v * np.sin(self.theta)

        self.obj.m_Position = self.position
       
    @staticmethod
    def SNR(d, r) :
        
        #Pt = 20 dBm
        
        sig = -80 # Watts
        u = 9.61
        b = 0.16
        nlos = 1 #dB
        nNlos = 20 #dB
        fc = 2 * 10**9 # Hz
        c = 299792458 # m/s
        
        h = d.position.y - 1 #m
        dist = np.sqrt(h**2 + r**2)
        
        if d.n_users > 0 :
           band = d.bandwidth / (d.n_users)
        else :
           band = d.bandwidth
        
    
        plos = 1 / (1 + u * np.exp( -1 * b * (np.degrees(np.arctan(h / r)) - u)))

        pNlos = 1 - plos

        lOS = 20*np.log10(4*np.pi*fc*dist / c) + nlos #dB
        nLOS = 20*np.log10(4*np.pi*fc*dist / c) + nNlos #dB

        l = lOS * plos + nLOS * pNlos #dB
        
        pr = (d.transmission_power - l) #dBm

        pr = 10 ** ((pr-30)/10)  #Watt
        sig = 10 ** ((sig-30)/10) #watt
        
        snr = pr / sig #Watt

        r = band * np.log2(1 + snr) * 10**-6  #Mbps

        snr = 10 * np.log10(snr) #db
        
        return snr, r