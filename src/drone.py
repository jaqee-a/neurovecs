from turtle import distance
import pygame
import numpy as np
import random

from regex import R

class Drone :

    color = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (50,200,0), (50,0,200), (20,20,100), (0,20,100)]
    i = 0

    def __init__ (self) :

        self.p = pygame.Vector3(800, 60, 600)
        self.theta = 0
        self.n_users = 0
        self.pt = 5 #Watt
        self.band = 100 * 10**6 #Hz
        self.con = []
        self.theta = 42.44
        self.capacity = 20
        #self.color = Drone.color[Drone.i]
        Drone.i += 1

    def meters(self) :

        return self.p / 6

    def r(self) :
        
        return (self.meters().z) / np.tan(np.radians(self.theta))

    def distance(self) :

        return np.sqrt(self.r()**2 + self.meters().z**2)

    def SNR(self) :

        avr = 0
        
        for p in self.con :
            avr += p.SNR(self)[1]
        
        return avr / len(self.con)

    def show(self, screen, font) :

        f = font.render(str(int(self.meters().z)), 1, pygame.Color("coral"))
        screen.blit(f, (self.p.x,self.p.y))
