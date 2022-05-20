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

    