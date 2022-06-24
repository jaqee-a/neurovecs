from operator import le
import pygame
from User import user
from drone import Drone
from readMap import draw, read
import matplotlib.pyplot as plt
import numpy as np
 
def drop2():

    rat = []
    con  = []
    ecar = []
    time = [0]

    user_n = 200
    drone_n = 7

    height, width = 700, 1300
    user_tr = 10
    non_con_user = user_n
    T = 2 #db

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
        d = Drone(pygame.Vector3(600, 250, 40))
        drone.append(d)

    stable = False
    iter = 0
    done = False


    def inService(drones):

        for i, dr in enumerate(drones) :
            if dr.n_users == 0 :
                return False, i
        return True, None

    def equilibrium(con, rate):

        et = np.std(con)
        er = np.std(rate)
        
        return et < 1 and er < 1 and non_con_user < user_n
        

    
    vel = [Drone.batteryCapacity*100/Drone.capacity]

    conne = [0 for _ in range(100)]
    rate  = [0 for _ in range(100)]


    running = True
    while running:
        
        non_con_user = user_n
        
        for u in users :
                u.isConnected = None

        for d in drone :
            d.n_users = 0
            d.con.clear()
            
            l = []
            for u in users :
                if u.isConnected == None :
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

        dar = [] 
        for u in users :
            if u.isConnected != None :
                dar.append(u.SNR(u.isConnected)[1])
            else :
                dar.append(0)  
    
        
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
            
            dt = F.normalize()
            d.p += dt
            
            """try :
                if i == 0 :
                v = dt.length() / (clock.get_time()*10**-3)
                e = d.EnergyConsumption(v)
                
                #amps = watts / volts
                c = (clock.get_time()*10**-3 / 3600) * e / Drone.batteryVoltage
                Drone.batteryCapacity -= (c * 1000)
                
                vel.append(Drone.batteryCapacity*100/Drone.capacity)

            except:
                vel.append(Drone.batteryCapacity*100/Drone.capacity)
        
        """
        conne[iter % 100] = (100 * (user_n - non_con_user))/user_n
        rate[iter % 100] = np.mean(dar)

        """if equilibrium(conne, rate) :
            dr_a = np.mean(dar)
            et = np.std(dar)
            con = 100 * (user_n - non_con_user) / user_n
                
            print(dr_a, con, et)
            running = False"""

        """if stable == True : 
        
            b, i = inService(drone)
            n_p = (non_con_user * 100) / user_n
            
            if n_p > user_tr and b == True :
            
            d = Drone()
            drone.insert(0, d)
            drone_n += 1
            stable = False"""
        
        t = time[-1] + clock.get_time()/1000
        if iter > 60 :
            if time[0] == 0 :
                time[0] = t
            else :
                time.append(t)
            rat.append(np.mean(dar))
            con.append(100 * (user_n - non_con_user)/user_n)
            ecar.append(np.std(dar))

        if t > 500 :
            return time, rat, con, ecar


        
        
        for u in users :
            u.randomWalk(iter, clock.get_time())

        iter += 1
        
        clock.tick(60)
        
