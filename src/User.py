from asyncio.windows_events import NULL
import random
from tkinter import W
from math import log2, sqrt
from turtle import isvisible
from cv2 import log
from matplotlib.style import use
import pygame
import numpy as np


class user :

    def __init__(self, height, width, obs) -> None:
        
        self.height, self.width = height, width
        a = random.choice([0,1])
        if a == 0 :
           self.u = pygame.Vector3(random.random() * 300 * 0.5 + 100, random.random() * 320 * 0.5 + 320, 0)
        else :
           self.u = pygame.Vector3(random.random() * 300 * 0.5 + 450, random.random() * 320 * 0.5 + 320, 0)
        self.v = random.uniform(1.25, 1.5) * 6
        #self.u = pygame.Vector3(random.randint(50, 650), random.randint(50, 650), 0)
        self.isConnected = NULL
        self.theta = 0
        self.beta = 0
        self.delta_theta = 0.3
        self.delta_t = 200
        self.obs = []
        for ob in obs :
            if ob[0].z == 0 :
               self.obs.append(pygame.Rect(ob[0].x-int(ob[1][0]/2), ob[0].y-int(ob[1][1]/2), ob[1][0], ob[1][1]))
        
        while self.isValid() == False :
              self.u = pygame.Vector3(random.randint(50, 650), random.randint(50, 650), 0)
              #self.u = pygame.Vector3(random.random() * 700 * 0.5, random.random() * 700 * 0.5, 0)
        

    def isValid(self):

        for ob in self.obs :
            if ob.collidepoint(self.u.x, self.u.y) == True :
                return False
                
        return True
    
    def randomWalk(self, iter, time) :
        
        
        v = self.v * time / 1000
    
        if iter % self.delta_t == 0 :
           a = random.randint(0, 360)
           self.theta = a * np.pi / 180

        elif self.isValid() == False :
           self.theta += np.pi
        
        elif self.u.x < 50 or self.u.x > 650 or self.u.y < 50 or self.u.y > 650 :
            self.theta += np.pi

        self.beta = random.uniform(0,1)
        self.delta_theta = 0.3 - 0.6 * self.beta

        self.theta += self.delta_theta

        self.u.x += v * np.cos(self.theta) 
        self.u.y += v * np.sin(self.theta) 

        

    def SNR(self, d) :
        
        #Pt = 5 Watt
        T = 2 # db
        sig = 10**-6 # Watts
        u = 9.61
        b = 0.16
        nlos = 1 #dB
        nNlos = 20 #dB
        fc = 3 * 10**9 # Hz
        c = 299792458 # m/s

        pt = 10 * np.log10(d.pt) + 30 #dBm
        
        dist = d.p.distance_to(self.u) / 6 #m
        h = d.p.z / 6 #m
        r = np.sqrt(dist**2 - h**2)
        band = d.band / (d.n_users + 1)
    
        plos = 1 / (1 + u * np.exp( -1 * b * (np.degrees(np.arctan(h / r)) - u)))

        pNlos = 1 - plos

        lOS = 20*np.log10(4*np.pi*fc*dist / c) + nlos #dB
        nLOS = 20*np.log10(4*np.pi*fc*dist / c) + nNlos #dB

        l = lOS * plos + nLOS * pNlos #dB
        
        pr = (pt - l) #dB

        pr = 10 ** (pr/10) #Watt

        snr = pr / sig

        r = band * np.log2(1 + snr) * 10**-6  #Mbps
        
        return snr, r