from operator import le
import pygame
from User import user
from drone import Drone
from readMap import draw, read
import matplotlib.pyplot as plt
import numpy as np
import random
 


pygame.init()


height, width = 700, 1300
user_tr = 10
T = 2 #db

user_n = 200
drone_n = 7
non_con_user = user_n

screen = pygame.display.set_mode((width, height))
wall = pygame.image.load("src\wall.png").convert_alpha()
clock = pygame.time.Clock()

#obstacle
obs = read()
obs = []

users = []
for _ in range(user_n):
    u = user(height, width, obs)
    users.append(u)

drone = []
for _ in range(drone_n):
    d = Drone()
    drone.append(d)

stable = False
iter = 0
done = False

alpha = 1

font = pygame.font.SysFont("Arial", 18)

def connected():
	return font.render("Connected :" +str(int((100 * (user_n - non_con_user))/user_n))+"%", 1, pygame.Color("coral"))

def deployed():
    return font.render("Drones :"+str(int(drone_n)), 1, pygame.Color("coral"))

def inService(drones):

    for i, dr in enumerate(drones) :
        if dr.n_users == 0 :
            return False
    return True

def equilibrium(con, rate):

    et = np.std(con)
    er = np.std(rate)
    
    return et < 0.1 and er < 0.1 and non_con_user < user_n
    

data = [0]
time = [0]
vel = [Drone.batteryCapacity]

conne = [0 for _ in range(100)]
rate  = [0 for _ in range(100)]

running = True
while running:
    screen.fill((0,0,0))
    draw(screen, wall, obs)

    if iter % 10 == 0 :
        txt = connected()
 
    screen.blit(txt, (300,10))
    screen.blit(deployed(), (500,10))
 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False

            fig, axs = plt.subplots(2)

            axs[0].plot(time, data)
            axs[1].plot(time, vel)
            
            axs[0].set(xlabel='Time (s)', ylabel='Data rate (Mbps)')
            axs[1].set(xlabel='Time (s)', ylabel='Energy (kW)')

            plt.show()

    
    for u in users :
        u.isConnected = None

    for d in drone :
        d.con.clear()
        d.n_users = 0
        d.q = 0
        d.f = pygame.Vector3(0)

    
        
    stable = True
    for d in drone :
        l = []
        for u in users :
            dist = u.p.distance_to(d.p)
            if u.isConnected == None and dist < 300 :  
                l.append([dist, u])

        l.sort(reverse= False,key=lambda x:x[0])
        i = 0
        while d.n_users < d.capacity and i < len(l) :
            l[i][1].isConnected = d
            d.con.append(l[i][1])
            d.n_users += 1
            i += 1
        
        d.q = 0.1 / (d.n_users + 1)

    for d in drone :
        for u in drone :
            if d.p != u.p :
                d.f += d.q * u.q *  (d.p - u.p).normalize() * 1 / ((u.p - d.p).length()**2)
        for u in users :
            if u.isConnected == d :
                d.f += d.q * u.q *  (d.p - u.p).normalize() * 1 / ((u.p - d.p).length()**2)

    for d in drone :
        if d.f.length() > 0 :
           d.p += 1 * d.f.normalize()
           d.p.z =40
        

    """n_p = (non_con_user * 100) / user_n
        
    if n_p > user_tr and equilibrium(conne, rate) and inService(drone):
        d = Drone()
        drone.insert(0, d)
        drone_n += 1
"""
    
        
    """try :
        if i == 0 :
            v = dt.length() / (clock.get_time()*10**-3)
            e = d.EnergyConsumption(v)
            
            #amps = watts / volts
            c = (clock.get_time()*10**-3 / 3600) * e / Drone.batteryVoltage
            print(c * 1000)
            Drone.batteryCapacity -= (c * 1000)
            
            vel.append(Drone.batteryCapacity)

    except:
            vel.append(Drone.batteryCapacity)"""

    
    non_con_user = user_n

    for i, d in enumerate(drone) :

        d.n_users = 0

        for u in d.con :
            snr = u.SNR(d)[0]   
            if snr > T :
                d.n_users += 1
                non_con_user -= 1
            else :
                u.isConnected = None     
        # pygame.draw.circle(screen, (0, 0 , 50), [d.p.x, d.p.y], d.r()*6)
        d.show(screen, font)
    
    
    dr = [] 
    for u in users :
        if u.isConnected != None :
           dr.append(u.SNR(u.isConnected)[1])
        else :
           dr.append(0)

    data.append(dr)
    time.append(time[-1] + clock.get_time()/1000)
    dat = font.render("data rate :"+str(int(np.mean(dr)))+" Mbps", 1, pygame.Color("coral"))
    screen.blit(dat, (10,10))

    et = font.render("Ecart type :"+str(int(np.std(dr))), 1, pygame.Color("coral"))
    screen.blit(et, (800,10))

    for u in users :
        
        u.show(screen)
    
    i = 0
    
    for u in users :

        u.randomWalk(iter, clock.get_time())

    conne[iter % 100] = (100 * (user_n - non_con_user))/user_n
    rate[iter % 100] = np.mean(dr)
    
    """if equilibrium(conne, rate) :
        dr_a = np.mean(dr)
        et = np.std(dr)
        con = 100 * (user_n - non_con_user) / user_n
            
        print(dr_a, con, et)
        running = False"""

    iter += 1
    
    clock.tick(60)
    pygame.display.update()