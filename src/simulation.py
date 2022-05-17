import random
from tkinter import W
from math import sqrt
import pygame
import numpy as np
from User import user
from drone import drone


from scipy import rand

pygame.init()

user_n = 100
drone_n = 1

height, width = 600, 800
user_tr = 10
non_con_user = 100
dist = 70
non_con = 0

theta = 20.34

screen = pygame.display.set_mode((width, height))

#obstacle
obs = []
#[pygame.Vector3(400, 350, 0), [100, 100]]

pop = []
for _ in range(user_n):
    p = user(0.001, height, width, obs)
    pop.append([p, 0])

drone_l = []
for _ in range(drone_n):
    d = drone(theta)
    drone_l.append(d)

stable = False
iter = 0

running = True
while running:
    screen.fill((0,0,0))
 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
    

    non_con_user = 100
    
    for p in pop :
            p[1] = 0
            for i, d in enumerate(drone_l):
                di = d.p.distance_to(p[0].u)
                if not p[1] and di < d.distance() :
                    print(d.SNR(di))
                    p[1] = 1
                    non_con_user -= 1
                    d.n_users += 1
                    break

    stable = True
    for d in drone_l:

        # Attraction force with the users
        F1 = pygame.Vector3(0, 0, 0)
        
        for p in pop:
            if not p[1] :
                v = p[0].u - d.p
                F1 += v.normalize() * 1 / (v.length() * (user_n/drone_n))
               
        # Repulsion force with other drones
        F2 = pygame.Vector3(0, 0, 0)

        for dr in drone_l:
            if d.p != dr.p : 
                v = d.p - dr.p
                F2 += v.normalize() * 1 / (v.length()*7)
            
            
        # Repulsion force with the obstacles
        F3 = pygame.Vector3(0, 0, 0)

        for ob in obs :
            v = d.p - ob[0]
            F3 += v.normalize() * 1 / (v.length()*2)

        # Repulsion force with the ground
        F4 = pygame.Vector3(0, 0, 1) * (1 / d.p.z**2)
        
        F = F1 + F2 + F3 + F4
        if F.length() > 0.001 :
            stable = False
            dt = F.normalize()
        
            d.p += dt
    
    if stable == True and non_con_user > 10  :
        
        stable = False
        drone_n += 1
        d = drone(theta)
        drone_l.insert(0, d)
    
    #print(drone_n)
    
    for i, d in enumerate(drone_l):

        #print(d.p.z)
        
        pygame.draw.circle(screen, (0, 0 , 50), [d.p.x, d.p.y], d.r())
        if d.p.z > 0 :
           pygame.draw.circle(screen, (0, 0 ,255), [d.p.x, d.p.y], 5)
        else :
            pygame.draw.circle(screen, (255, 255, 255), [d.p.x, d.p.y], 5)
        
    for p in pop :
        if p[1] == 0:
           pygame.draw.circle(screen, (255, 0, 0), [p[0].u.x, p[0].u.y], 2)
        else:
           pygame.draw.circle(screen, (0, 255, 0), [p[0].u.x, p[0].u.y], 2)
    
    
    i = 0
    for p in pop :

        p[0].randomWalk(iter)

    iter += 1

    for ob in pop[0][0].obs :
        pygame.draw.rect(screen, (255,255,255), ob)

    pygame.display.update()
    