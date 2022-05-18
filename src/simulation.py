from asyncio.windows_events import NULL
from pickletools import read_string1
import random
from tkinter import W
from math import sqrt
import pygame
import numpy as np
from User import user
from drone import Drone
from readMap import draw, read

pygame.init()

user_n = 100
drone_n = 1

height, width = 700, 960
user_tr = 10
non_con_user = 100
dist = 70
non_con = 0
theta = 20.34

screen = pygame.display.set_mode((width, height))
wall = pygame.image.load("wall.png").convert_alpha()

#obstacle
obs = read()

pop = []
for _ in range(user_n):
    p = user(0.001, height, width, obs)
    pop.append([p, 0])

drone = []
for _ in range(drone_n):
    d = Drone()
    drone.append(d)

dm = pygame.Vector3(0,0,0)
stable = False
iter = 0

font = pygame.font.SysFont("Arial", 18)

def connected():
	return font.render(str(int(100 - non_con_user))+"%", 1, pygame.Color("coral"))

def deployed():
    return font.render(str(int(drone_n)), 1, pygame.Color("coral"))

def inService(drones):

    for i, dr in enumerate(drones) :
        if dr.n_users == 0 :
            return False, i
    return True, NULL


txt = connected()

running = True
while running:
    screen.fill((0,0,0))
    draw(screen, wall, obs)

    if iter % 10 == 0 :
        txt = connected()
    screen.blit(txt, (590,40))
    screen.blit(deployed(), (700,40))
 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
    
    
    non_con_user = 100

    for d in drone :
        d.n_users = 0
    
    for p in pop :
            p[1] = 0
            for i, d in enumerate(drone):
                di = d.p.distance_to(p[0].u)
                if not p[1] and di < dist :
                    p[1] = 1
                    non_con_user -= 1
                    d.n_users += 1
                    break
                    

    stable = True
    for i, d in enumerate(drone) :

        F1 = pygame.Vector3(0, 0, 0)
        
        for p in pop:
            if not p[1] :
                v = p[0].u - d.p
                F1 += v.normalize() * 1 / (v.length() * (user_n/drone_n))
               

        F2 = pygame.Vector3(0, 0, 0)

        for dr in drone:
            if d.p != dr.p : 
                v = d.p - dr.p
                F2 += v.normalize() * 1 / (v.length()*7)
            
            
        
        F3 = pygame.Vector3(0, 0, 0)

        for ob in obs :
            v = d.p - ob[0]
            F3 += v.normalize() * 1 / (v.length()**2)
        

        F4 = pygame.Vector3(0, 0, 1) * (1 / d.p.z**2)
        
        F = F1 + F2 + F3 + F4
        #print(i, ":" , F.length())
        if d.n_users < 5 :
            stable = False
        dt = F.normalize()
        
        d.p += dt*2
    
    if stable == True : 
        
        stable = False
        b, i = inService(drone)
        print(b,i)
        if non_con_user > 10 and b == True :
           
           d = Drone()
           drone.insert(0, d)
           drone_n += 1

        elif b == False :
            
            #print(drone[i].n_users)
            drone.pop(i)
            drone_n -= 1
            print("deleted")
            

    
    #print(drone_n)
    
    for i, d in enumerate(drone):
        
        try:
           r = sqrt(dist**2 - d.p.z**2)
           #print(i, ":", d.p.z)
           #r = d.z / np.tan(np.radians(theta))
        except:
            #print(i, ":", d.z)
            a=0
            """if d.p.z > 300 :
               drone.pop(0)
               drone_n -= 1
               non_con = non_con_user"""
            #print(drone_n)

        
        pygame.draw.circle(screen, (0, 0 , 50), [d.p.x, d.p.y], r)
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
    pygame.display.update()
    