import random
from tkinter import W
from math import sqrt
import pygame
import numpy as np


from scipy import rand

pygame.init()

user_n = 100
drone_n = 1

height, width = 600, 800
user_tr = 10
non_con_user = 100
dist = 70
dx, dy = 0.01, 0.01
non_con = 0

dp = [(np.random.random(), np.random.random()) for i in range(100)]

screen = pygame.display.set_mode((width, height))

pop = []
for _ in range(user_n):
    p = pygame.Vector3(random.random() * width* 0.5 + 200, random.random() * height* 0.5 + 200, 0)
    pop.append([p, 0])

drone = []
for _ in range(drone_n):
    d = pygame.Vector3(50, 50, 20)
    drone.append(d)

dm = pygame.Vector3(0,0,0)
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
            for i, d in enumerate(drone):
                di = d.distance_to(p[0])
                if not p[1] and di < dist :
                    p[1] = 1
                    non_con_user -= 1
    
    for d in drone:

        F1 = pygame.Vector3(0, 0, 0)
        F3 = pygame.Vector3(0, 0, 0)
        for p in pop:
            #print(p[0])
            if not p[1] :
                v = p[0] - d
                v.z = 0
                F1 += v.normalize() * 1 / (v.length() * (user_n/drone_n))
                #F3 += v.normalize() * -1 / (v.length() * (user_n/drone_n)**2)
            
            #F1 = F1 / drone_n   
            #F3 = F3 / drone_n
            #F1 = F1.normalize()
            

        F2 = pygame.Vector3(0, 0, 0)
        for dr in drone:
            if d != dr : 
                v = d - dr
                v.z = 0
                F2 += v.normalize() * 1 / (v.length()**2)
            
            #F2 = F2.normalize()
            
        F = F1 + F2
        dt = F.normalize()
            
        d += dt
        #d1.append(dt)
        
    if non_con_user > 10 and stable == False :

        if iter % 20 == 0 :

            if (dm - drone[0]).length() < 1 :
                stable = True
            elif drone[0].x < 0 or drone[0].y < 0:
                drone.pop(0)
                drone_n -= 1
                non_con = non_con_user

            dm.x, dm.y, dm.z = drone[0].x, drone[0].y, drone[0].z
    

    elif stable == True and non_con_user > non_con + 5:
        
        stable = False
        drone_n += 1
        d = pygame.Vector3(50 , 50 , 20)
        drone.insert(0, d)
    
    print(drone_n)
    
    for i, d in enumerate(drone):
        
        try:
           r = sqrt(dist**2 - d.z**2)
           #print(i, ":", d.z)
        except:
            print(i, ":", d.z)
            non_con_user = 0
            break

        
        pygame.draw.circle(screen, (0, 0 , 50), [d.x, d.y], r)
        if d.z > 0 :
           pygame.draw.circle(screen, (0, 0 ,255), [d.x, d.y], 5)
        else :
            pygame.draw.circle(screen, (255, 255, 255), [d.x, d.y], 5)
        
    for p in pop :
        if p[1] == 0:
           pygame.draw.circle(screen, (255, 0, 0), [p[0].x, p[0].y], 2)
        else:
           pygame.draw.circle(screen, (0, 255, 0), [p[0].x, p[0].y], 2)
    
    
    i = 0
    for p in pop :

        p[0] = p[0] + pygame.Vector3(dp[i][0]*.01, dp[i][1]*.01, 0)
        
        i+=1
        
        """if p[0].x > 780 or p[0].x < 20 :
            dx *= -1
            break
        elif p[0].y > 580 or p[0].y < 20 :
            dy *= -1
            break
        """
    iter += 1
    pygame.display.update()
    