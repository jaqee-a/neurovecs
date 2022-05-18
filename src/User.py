import random
from tkinter import W
from math import sqrt
from turtle import isvisible
import pygame
import numpy as np


class user :

    def __init__(self, velocity, height, width, obs) -> None:
        
        self.height, self.width = height, width
        self.u = pygame.Vector3(random.random() * 704 * 0.5 + 256, random.random() * 320 * 0.5 + 320, 0)
        self.v = velocity
        self.theta = 0
        self.beta = 0
        self.delta_theta = 0.3
        self.delta_t = 100
        self.obs = []
        for ob in obs :
            if ob[0].z == 0 :
               self.obs.append(pygame.Rect(ob[0].x-ob[1][0], ob[0].y-ob[1][1], ob[1][0], ob[1][1]))
        
        while self.isValid() == False :
              self.u = pygame.Vector3(random.random() * 704 * 0.5 + 32, random.random() * 320 * 0.5 + 320, 0)
        

    def isValid(self):

        for ob in self.obs :
            if ob.collidepoint(self.u.x, self.u.y) :
                return False
        return True
    
    def randomWalk(self, iter) :
    
        if iter % self.delta_t == 0 :
           a = random.randint(0, 360)
           self.theta = a * np.pi / 180

        elif self.u.x < 224 or self.u.x > 768 or self.u.y < 224 or self.u.y > 544 \
           or self.isValid() == False :

           self.theta += np.pi

        self.beta = random.uniform(0,1)
        self.delta_theta = 0.3 - 0.6 * self.beta

        self.theta += self.delta_theta

        self.u.x += self.v * np.cos(self.theta) * self.delta_t
        self.u.y += self.v * np.sin(self.theta) * self.delta_t

        

   