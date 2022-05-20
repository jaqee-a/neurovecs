import random
from tkinter import W
from math import log2, sqrt
from turtle import isvisible
from cv2 import log
import pygame
import numpy as np


class user :

    def __init__(self, velocity, height, width, obs) -> None:
        
        self.height, self.width = height, width
        a = random.choice([0,1])
        if a == 0 :
           self.u = pygame.Vector3(random.random() * 300 * 0.5 + 100, random.random() * 320 * 0.5 + 320, 0)
        else :
           self.u = pygame.Vector3(random.random() * 300 * 0.5 + 450, random.random() * 320 * 0.5 + 320, 0) 
        self.v = velocity
        
        self.theta = 0
        self.beta = 0
        self.delta_theta = 0.3
        self.delta_t = 200
        self.obs = []
        for ob in obs :
            if ob[0].z == 0 :
               self.obs.append(pygame.Rect(ob[0].x-int(ob[1][0]/2), ob[0].y-int(ob[1][1]/2), ob[1][0], ob[1][1]))
        
        while self.isValid() == False :
              self.u = pygame.Vector3(random.random() * 704 * 0.5 + 32, random.random() * 320 * 0.5 + 320, 0)
        

    def isValid(self):

        for ob in self.obs :
            if ob.collidepoint(self.u.x, self.u.y) == True :
                return False
                
        return True
    
    def randomWalk(self, iter) :
    
        if iter % self.delta_t == 0 :
           a = random.randint(0, 360)
           self.theta = a * np.pi / 180

        elif self.isValid() == False :
           self.theta += np.pi

        self.beta = random.uniform(0,1)
        self.delta_theta = 0.3 - 0.6 * self.beta

        self.theta += self.delta_theta

        self.u.x += self.v * np.cos(self.theta) * self.delta_t
        self.u.y += self.v * np.sin(self.theta) * self.delta_t

        

    def SNR(self, d) :

        T = 2 # db
        sig = 1 / (10**6) # Watts
        u = 9.61
        b = 0.16
        nlos = 1 #dB
        nNlos = 20 #dB
        fc = 2.5 * 10**9 # Hz
        c = 299792458 # m/s
        a = 2 
        
        dist = d.p.distance_to(self.u)
        r1 = np.sqrt(dist**2 - d.p.z**2)
    
        plos = 1 / (1 + u * np.exp( -1 * b * (np.degrees(np.arctan(d.p.z / r1)) - u)))

        pNlos = 1 - plos

        lOS = 20*np.log10(4*np.pi*fc*dist / c) + nlos
        nLOS = 20*np.log10(4*np.pi*fc*dist / c) + nNlos

        l = lOS * plos + nLOS * pNlos

        pr = d.pt - l
        
        print(pr / sig)

