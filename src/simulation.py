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

height, width = 700, 700
user_tr = 10
non_con_user = user_n
dist = 120

screen = pygame.display.set_mode((width, height))
wall = pygame.image.load("src\wall.png").convert_alpha()
clock = pygame.time.Clock()

#obstacle
obs = read()
obs = []

pop = []
for _ in range(user_n):
    p = user(height, width, obs)
    pop.append(p)

drone = []
for _ in range(drone_n):
    d = Drone()
    drone.append(d)

stable = False
iter = 0

font = pygame.font.SysFont("Arial", 18)

def connected():
	return font.render(str(int((100 * (user_n - non_con_user))/user_n))+"%", 1, pygame.Color("coral"))

def deployed():
    return font.render(str(int(drone_n)), 1, pygame.Color("coral"))

def inService(drones):

    for i, dr in enumerate(drones) :
        if dr.n_users == 0 :
            return False, i
    return True, NULL


running = True
while running:
    screen.fill((0,0,0))
    draw(screen, wall, obs)

    if iter % 10 == 0 :
        txt = connected()
 
    screen.blit(txt, (300,10))
    screen.blit(deployed(), (350,10))
 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
    
    
    non_con_user = user_n
    
    for p in pop :
            p.isConnected = NULL

    for d in drone :
        d.n_users = 0
        d.con.clear()
        
        l = []
        for p in pop :
            if p.isConnected == NULL and d.n_users < d.capacity :
                snr = p.SNR(d)[0]
                if snr > 10 :
                    l.append([snr, p])
        l.sort(reverse= True)
        i = 0
        while i < d.capacity and i < len(l) :
            l[i][1].isConnected = d
            non_con_user -= 1
            d.n_users += 1
            d.con.append(l[i][1])
            i += 1

    
    dr = 0 
    for d in drone :
        if d.n_users > 0 :
            dr += d.SNR()
    
    dat = font.render(str(int(dr / drone_n)), 1, pygame.Color("coral"))
    screen.blit(dat, (80,10))
    
    
    stable = True
    for i, d in enumerate(drone) :

        # Attraction force with the users
        F1 = pygame.Vector3(0, 0, 0)
        
        for p in pop:
            if p.isConnected == NULL :
                v = p.u - d.p
                F1 += v.normalize() * 1 / (v.length() * (user_n/drone_n))
                #F1 += v
        
        #F1 = F1.normalize() * 1 / (user_n / drone_n)
               
        # Repulsion force with other drones
        F2 = pygame.Vector3(0, 0, 0)

        for dr in drone:
            if d.p != dr.p :  
                v = d.p - dr.p
                F2 += v.normalize() * 1 / (v.length()*9)
            
            
        # Repulsion force with the obstacles
        F3 = pygame.Vector3(0, 0, 0)

        for ob in obs :
            v = d.p - ob[0]
            F3 += v.normalize() * 0.6 / (v.length()**2)
        
        # Repulsion force with the ground
        F4 = pygame.Vector3(0, 0, 1) * (1 / d.p.z**2)
        
        F = F1 + F2 + F3 + F4
        #print(i, ":" , F.length())
        if F.length() > 0.001  :
            stable = False
        else :
            print(i, ":" , F.length())

        dt = F.normalize()
        
        d.p += dt*2
    
    if stable == True :           
        
        stable = False
        b, i = inService(drone)
        
        if non_con_user > 10 and b == True :
           
           d = Drone()
           drone.insert(0, d)
           drone_n += 1

        """elif b == False :
            
            #print(drone[i].n_users)
            drone.pop(i)
            drone_n -= 1
            print("deleted")"""
            
    for i, d in enumerate(drone) :
        
        pygame.draw.circle(screen, (0, 0 , 50), [d.p.x, d.p.y], d.r()*6)
        if d.p.z > 0 :
           pygame.draw.circle(screen, (0, 0 ,255), [d.p.x, d.p.y], 5)
        else :
            pygame.draw.circle(screen, (255, 255, 255), [d.p.x, d.p.y], 5)
        
        d.show(screen, font)
        
    for p in pop :
        
        if p.isConnected == NULL:
           pygame.draw.circle(screen, (255, 255, 255), [p.u.x, p.u.y], 2)
        else:
           pygame.draw.circle(screen, p.isConnected.color, [p.u.x, p.u.y], 2)
    
    
    i = 0
    
    for p in pop :

        p.randomWalk(iter, clock.get_time())

    iter += 1
    
    clock.tick(60)
    pygame.display.update()
    