from operator import le
import pygame
from User import user
from drone import Drone
from readMap import draw, read
import matplotlib.pyplot as plt
import numpy as np
import random
 
def drop() :

    rat = []
    con  = []
    ecar = []
    time = [0]

    height, width = 700, 1300
    user_tr = 10
    T = 2 #db

    user_n = 100
    drone_n = 6
    non_con_user = user_n

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
        d = Drone(pygame.Vector3(300, 250, 40))
        drone.append(d)

    iter = 0
    

    def equilibrium(con, rate):

        et = np.std(con)
        er = np.std(rate)

        return et < 0.1 and er < 0.1 and non_con_user < user_n

    vel = [Drone.batteryCapacity]

    conne = [0 for _ in range(100)]
    rate  = [0 for _ in range(100)]


    running = True
    while running:
        
        for u in users :
            u.isConnected = None

        for d in drone :
            d.con.clear()
            d.n_users = 0
            d.q = 0
            d.f = pygame.Vector3(0)

        
        for d in drone :
            l = []
            for u in users :
                dist = u.p.distance_to(d.p)
                if u.isConnected == None and dist < 400 :  
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
        

        """data.append(dr)
        time.append(time[-1] + clock.get_time()/1000)
        """
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

        dr = [] 
        for u in users :
            if u.isConnected != None :
                dr.append(u.SNR(u.isConnected)[1])
            else :
                dr.append(0) 

            
        for u in users :
            u.randomWalk(iter, clock.get_time())

        conne[iter % 100] = (100 * (user_n - non_con_user))/user_n
        rate[iter % 100] = np.mean(dr)

        """if equilibrium(conne, rate) :
            dr_a = np.mean(dr)
            et = np.std(dr)
            con = 100 * (user_n - non_con_user) / user_n
            return dr_a, con, et"""

        t = time[-1] + clock.get_time()/1000
        if iter > 60 :
            if time[0] == 0 :
                time[0] = t
            else :
                time.append(t)
            rat.append(np.mean(dr))
            con.append(100 * (user_n - non_con_user)/user_n)
            ecar.append(np.std(dr))

        if t > 500 :
            return time, rat, con, ecar

        iter += 1
        
        clock.tick(60)
        
