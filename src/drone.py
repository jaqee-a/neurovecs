from turtle import distance
import pygame
import numpy as np

dist = 70

class Drone :

    def __init__ (self, theta) :

        self.p = pygame.Vector3(800, 60, 20)
        self.theta = theta
        self.n_users = 0
        self.pt = 30

    def r(self) :
        
        return self.p.z / np.tan(np.radians(self.theta))

    def distance(self) :

        return min(dist, np.sqrt(self.r()**2 + self.p.z**2))

    def SNR(self, d) :

        T = 2 # db
        sig = 1 / 10**6 # Watts
        u = 9.61
        b = 0.16
        nlos = 1
        nNlos = 20
        fc = 2.5 * 10**9 # GHz
        c = 299792458 # m/s
        a = 2 

        r1 = np.sqrt(d**2 - self.p.z**2)
    
        plos2 = 1 / (1 + u * np.exp( -1 * b * (np.arctan(self.p.z / r1) - u)))

        plos = 1 / (1 + u * np.exp( -1 * b * (180/np.pi * np.arctan(self.p.z / r1) - u)))
        pNlos = 1 - plos

        lOS = 20*np.log10(4*np.pi*fc*d / c) + nlos
        nLOS = 20*np.log10(4*np.pi*fc*d / c) + nNlos

        l = lOS * plos + nLOS * pNlos

        pr = self.pt - l
        
        return pr

