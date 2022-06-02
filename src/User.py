from asyncio.windows_events import NULL
import random
from tkinter import W
from math import log2, sqrt
from turtle import isvisible
from cv2 import log
from matplotlib.style import use
import pygame
import numpy as np

from drone import Drone


class user :

    def __init__(self, height, width, obs) -> None:
        
        self.height, self.width = height, width
        a = random.choice([0,1])
        """if a == 0 :
           self.p = pygame.Vector3(random.random() * 300 * 0.5 + 100, random.random() * 320 * 0.5 + 320, 0)
        else :
           self.p = pygame.Vector3(random.random() * 300 * 0.5 + 450, random.random() * 320 * 0.5 + 320, 0)"""
        self.v = random.uniform(1.25, 1.5) # m/s
        self.p = pygame.Vector3(random.randint(0, 100), random.randint(0, 100), 0)
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
              self.u = pygame.Vector3(random.randint(0, 100), random.randint(0, 100), 0)
              #self.u = pygame.Vector3(random.random() * 700 * 0.5, random.random() * 700 * 0.5, 0)

    def isValid(self):

        for ob in self.obs :
            if ob.collidepoint(self.p.x, self.p.y) == True :
                return False
                
        return True
    
    def randomWalk(self, iter, time) :
        
        
        v = self.v * time / 1000
    
        if iter % self.delta_t == 0 :
           a = random.randint(0, 360)
           self.theta = a * np.pi / 180

        elif self.isValid() == False :
           self.theta += np.pi
        
        elif self.p.x < 0 or self.p.x > 100 or self.p.y < 0 or self.p.y > 100 :
            self.theta += np.pi

        self.beta = random.uniform(0,1)
        self.delta_theta = 0.3 - 0.6 * self.beta

        self.theta += self.delta_theta

        self.p.x += v * np.cos(self.theta) 
        self.p.y += v * np.sin(self.theta) 

        

    def SNR(self, d) :
        
        #Pt = 20 dBm
        
        sig = -80 # Watts
        u = 9.61
        b = 0.16
        nlos = 1 #dB
        nNlos = 20 #dB
        fc = 2 * 10**9 # Hz
        c = 299792458 # m/s
        
        dist = d.p.distance_to(self.p) #m
        h = d.p.z #m
        r = np.sqrt(dist**2 - h**2)
        
        
        if d.n_users > 0 :
           band = d.band / (d.n_users)
        else :
           band = d.band
        
    
        plos = 1 / (1 + u * np.exp( -1 * b * (np.degrees(np.arctan(h / r)) - u)))

        pNlos = 1 - plos

        lOS = 20*np.log10(4*np.pi*fc*dist / c) + nlos #dB
        nLOS = 20*np.log10(4*np.pi*fc*dist / c) + nNlos #dB

        l = lOS * plos + nLOS * pNlos #dB
        
        pr = (d.pt - l) #dBm

        pr = 10 ** ((pr-30)/10)  #Watt
        sig = 10 ** ((sig-30)/10) #watt
        
        snr = pr / sig #Watt

        r = band * np.log2(1 + snr) * 10**-6  #Mbps

        snr = 10 * np.log10(snr) #db
        
        return snr, r
