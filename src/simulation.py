import random
from tkinter import W
from math import sqrt
import pygame
import numpy as np
from User import user


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
obs = [[pygame.Vector3(200, 350, 0), [100, 100]],[pygame.Vector3(300, 350, 0), [100, 100]], [pygame.Vector3(250, 100, 0), [50, 50]],[pygame.Vector3(250, 150, 0), [50, 50]],[pygame.Vector3(400, 350, 0), [100, 100]],[pygame.Vector3(400, 250, 0), [100, 100]],[pygame.Vector3(400, 150, 0), [100, 100]]]

pop = []
for _ in range(user_n):
    p = user(0.001, height, width, obs)
    pop.append([p, 0])

drone = []
for _ in range(drone_n):
    d = pygame.Vector3(200, 200, 20)
    drone.append(d)

dm = pygame.Vector3(0,0,0)
stable = False
iter = 0

font = pygame.font.SysFont("Arial", 18)
def update():
	
	text = font.render(str(int(100 - non_con_user))+"%", 1, pygame.Color("coral"))
	return text

running = True
while running:
    screen.fill((0,0,0))
    screen.blit(update(), (590,0))
 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
    
    

    non_con_user = 100
    
    for p in pop :
            p[1] = 0
            for i, d in enumerate(drone):
                di = d.distance_to(p[0].u)
                if not p[1] and di < dist :
                    p[1] = 1
                    non_con_user -= 1

    stable = True
    for d in drone:

        F1 = pygame.Vector3(0, 0, 0)
        
        for p in pop:
            if not p[1] :
                v = p[0].u - d
                F1 += v.normalize() * 1 / (v.length() * (user_n/drone_n))
               

        F2 = pygame.Vector3(0, 0, 0)

        for dr in drone:
            if d != dr : 
                v = d - dr
                F2 += v.normalize() * 1 / (v.length()*7)
            
            
        
        F3 = pygame.Vector3(0, 0, 0)

        for ob in obs :
            v = d - ob[0]
            F3 += v.normalize() * 1 / (v.length()*6)

        F4 = pygame.Vector3(0, 0, 1) * (1 / d.z**2)
        
        F = F1 + F2 + F3 + F4
        if F.length() > 0.001 :
            stable = False
            dt = F.normalize()
        
            d += dt
    
    if stable == True and non_con_user > non_con + 5:
        
        stable = False
        drone_n += 1
        d = pygame.Vector3(50 , 50 , 20)
        drone.insert(0, d)
    
    #print(drone_n)
    
    for i, d in enumerate(drone):
        
        try:
           r = sqrt(dist**2 - d.z**2)
           #print(i, ":", d.z)
           #r = d.z / np.tan(np.radians(theta))
        except:
            #print(i, ":", d.z)
            if d.z > 300 :
               drone.pop(0)
               drone_n -= 1
               non_con = non_con_user
            #print(drone_n)

        
        pygame.draw.circle(screen, (0, 0 , 50), [d.x, d.y], r)
        if d.z > 0 :
           pygame.draw.circle(screen, (0, 0 ,255), [d.x, d.y], 5)
        else :
            pygame.draw.circle(screen, (255, 255, 255), [d.x, d.y], 5)
        
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
    