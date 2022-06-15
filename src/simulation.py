from operator import le
import pygame
from User import user
from drone import Drone
from readMap import draw, read
import matplotlib.pyplot as plt
import numpy as np
 


pygame.init()

user_n = 100
drone_n = 1

height, width = 700, 1300
user_tr = 10
non_con_user = user_n
T = 15 #db

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

font = pygame.font.SysFont("Arial", 18)

def connected():
	return font.render("Connected :" +str(int((100 * (user_n - non_con_user))/user_n))+"%", 1, pygame.Color("coral"))

def deployed():
    return font.render("Drones :"+str(int(drone_n)), 1, pygame.Color("coral"))

def inService(drones):

    for i, dr in enumerate(drones) :
        if dr.n_users == 0 :
            return False, i
    return True, None

data = [0]
time = [0]
vel = [Drone.batteryCapacity*100/Drone.capacity]


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
            axs[1].set(xlabel='Time (s)', ylabel='Battery (%')
            #axs[1].set_ylim([0,100])

            plt.show()
            
    
    non_con_user = user_n
    
    for u in users :
            u.isConnected = None

    for d in drone :
        d.n_users = 0
        d.con.clear()
        
        l = []
        for u in users :
            if u.isConnected == None and d.n_users < d.capacity :
                snr = u.SNR(d)[0]
                
                if snr > T :
                    l.append([snr, u])
        l.sort(reverse= True,key=lambda x:x[0])
        i = 0
        while i < d.capacity and i < len(l) :
            if l[i][0] > T :
               l[i][1].isConnected = d
               non_con_user -= 1
               d.n_users += 1
               d.con.append(l[i][1])
               i += 1
            else :
                break

    
    dr = 0 
    for u in users :
        if u.isConnected != None :
           dr += u.SNR(u.isConnected)[1]

    dr = dr / user_n
    
    e = 0
    for u in users :
        if u.isConnected != None :
            e += (u.SNR(u.isConnected)[1] - dr)**2
        else :
            e += (0 - dr)**2

    e = np.sqrt(e / user_n)

    data.append(dr)
    time.append(time[-1] + clock.get_time()/1000)
    dat = font.render("data rate :"+str(int(dr))+" Mbps", 1, pygame.Color("coral"))
    screen.blit(dat, (10,10))

    et = font.render("Ecart type :"+str(int(e)), 1, pygame.Color("coral"))
    screen.blit(et, (800,10))
    
    
    stable = True
    for i, d in enumerate(drone) :

        # Attraction force with the users
        F1 = pygame.Vector3(0, 0, 0)
        
        for u in users:
            if u.isConnected == None :
                v = u.p - d.p
                F1 += v.normalize() * (1 - 1 / v.length()) * (1 / non_con_user)
                
        #F1 = F1 * 1 / user_n
        

        # Repulsion force with other drones
        F2 = pygame.Vector3(0, 0, 0)

        for dr in drone:
            if d.p != dr.p :  
                v = d.p - dr.p
                F2 += v.normalize() * (1 / v.length() ) * non_con_user

    
        # Repulsion force with the obstacles
        F3 = pygame.Vector3(0, 0, 0)
        
        for ob in obs :
            v = ((d.p * 6) + pygame.Vector3(50, 50, 0)) - ob[0]
            F3 += v.normalize() * 1 / (v.length()**2)


        # Repulsion force with the ground 
        F4 = pygame.Vector3(0, 0, 1) *  1 / (d.p.z ** 2) * user_n

        
        #F4 = (F1 - (F1 + F4)) * (-lamb)

        F = F1 + F2 + F3 + F4
        
       
        """ #c = pygame.Vector3(0)
        for u in d.con:
            c += u.p
        
        if d.n_users > 0:
            c = c / d.n_users

            a = (c-d.p).length()
        else:
            a = 51

        pygame.draw.line(screen, (0, 255, 0), (d.p.x, d.p.y), (c.x, c.y), 1)#"""
                
        #print(i, ":" , dt.length())
        #if a > 50:
        print(F.length())
        if F.length() > 0.01 :
            stable = False

        
        dt = F.normalize()
        d.p += dt
        
        try :
            if i == 0 :
               v = dt.length() / (clock.get_time()*10**-3)
               e = d.EnergyConsumption(v)
               
               #amps = watts / volts
               c = (clock.get_time()*10**-3 / 3600) * e / Drone.batteryVoltage
               Drone.batteryCapacity -= (c * 1000)
               
               vel.append(Drone.batteryCapacity*100/Drone.capacity)

        except:
               vel.append(Drone.batteryCapacity*100/Drone.capacity)
    
    if stable == True : 
    
        b, i = inService(drone)
        n_p = (non_con_user * 100) / user_n
        
        if n_p > user_tr and b == True :
        
           d = Drone()
           drone.insert(0, d)
           drone_n += 1
           stable = False
        
            
                        
    for i, d in enumerate(drone) :
        
        # pygame.draw.circle(screen, (0, 0 , 50), [d.p.x, d.p.y], d.r()*6)
        
        if d.p.z > 0 :
           pygame.draw.circle(screen, (0, 0 ,255), [d.p.x*6+50, d.p.y*6+50], 5)
        else :
            pygame.draw.circle(screen, (255, 255, 255), [d.p.x*6+50, d.p.y*6+50], 5)
        
        d.show(screen, font)
        
    for u in users :
        
        if u.isConnected == None:
           pygame.draw.circle(screen, (255, 255, 255), [u.p.x*6+50, u.p.y*6+50], 2)
        else:
           pygame.draw.circle(screen, u.isConnected.color, [u.p.x*6+50, u.p.y*6+50], 2)
    
    
    i = 0
    
    for u in users :

        u.randomWalk(iter, clock.get_time())

    iter += 1
    
    clock.tick(60)
    pygame.display.update()