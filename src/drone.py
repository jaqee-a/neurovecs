import pygame
import numpy as np


class drone :

    def __init__ (self, theta) :

        self.p = pygame.Vector3(50, 50, 30)
        self.theta = theta
        self.n_users = 0

    def r(self) :
        
        return self.p.z / np.tan(np.radians(self.theta))

    def distance(self) :

        return np.sqrt(self.r()**2 + self.p.z**2)