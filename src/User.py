import random
from tkinter import W
from math import sqrt
import pygame
import numpy as np


height, width = 600, 800
screen = pygame.display.set_mode((width, height))
iter = 0

pygame.init()

v = 0.01
theta = 0
beta = 0
delta_theta = 0.3
delta_t = 100

u = pygame.Vector3(300, 400, 0)

running = True
while running:
    #screen.fill((0,0,0))
 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
    
    if iter % delta_t == 0 or u.x < 0 or u.y < 0 or u.x > width or u.y > height :
        a = random.randint(0, 360)
        theta = a * np.pi / 180

    beta = random.uniform(0,1)
    delta_theta = 0.3 - 0.6 * beta

    theta += delta_theta

    u.x += v * np.cos(theta) * delta_t
    u.y += v * np.sin(theta) * delta_t

    pygame.draw.circle(screen, (255, 255, 255), [u.x, u.y], 2)

    iter += 1
    pygame.display.update()
