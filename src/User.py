import random
from tkinter import W
from math import sqrt
import pygame
import numpy as np


class user :

    def __init__(self, h, w) -> None:
        
        self.height, self.width = h, w
        self.u = pygame.Vector3(random.random() * self.width* 0.5 + 200, random.random() * self.height* 0.5 + 200, 0)
        self.v = 0.01
        self.theta = 0
        self.beta = 0
        self.delta_theta = 0.3
        self.delta_t = 100


    def randomWalk(self) :
    
        if iter % self.delta_t == 0 or self.u.x < 0 or self.u.x > self.width or self.u.y < 0 or self.u.y > self.height :
           a = random.randint(0, 360)
           theta = a * np.pi / 180

        beta = random.uniform(0,1)
        delta_theta = 0.3 - 0.6 * beta

        theta += delta_theta

        self.u.x += self.v * np.cos(theta) * self.delta_t
        self.u.y += self.v * np.sin(theta) * self.delta_t

        return self.u

   