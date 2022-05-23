from turtle import distance
import pygame
import numpy as np

dist = 70

class Drone :

    def __init__ (self) :

        self.p = pygame.Vector3(800, 60, 20)
        self.theta = 0
        self.n_users = 0
        self.pt = 5 #Watt
        self.band = 100 * 10**6 #Hz
        self.con = []
        self.theta = 42.44

    def r(self) :
        
        return self.p.z / np.tan(np.radians(self.theta))

    def distance(self) :

        return np.sqrt(self.r()**2 + self.p.z**2)

    def SNR(self) :

        avr = 0
        
        for p in self.con :
            avr += p.SNR(self)
        
        return avr / len(self.con)
