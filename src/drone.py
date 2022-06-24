from turtle import distance
import pygame
import numpy as np
import random

from regex import R

class Drone :

    color = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (50,200,0), (50,0,200), (20,20,100), (0,20,100)]
    i = 0
    
    batteryCapacity = 22000 #mAh
    capacity = batteryCapacity
    batteryVoltage = 51.8 #v

    def __init__ (self, p) :
        
        self.p = p # meters
        self.theta = 0
        self.n_users = 0
        self.pt = 20 # db
        self.band = 100 * 10**6 #Hz
        self.con = []
        self.theta = 42.44
        self.capacity = 30
        self.color = Drone.color[Drone.i % 10]
        Drone.i += 1 

        self.q = 0
        self.f = pygame.Vector3(0)  

    def r(self) :
        
        return (self.z) / np.tan(np.radians(self.theta))

    def distance(self) :

        return np.sqrt(self.r()**2 + self.z**2)

    def SNR(self) :

        avr = 0
        
        for p in self.con :
            avr += p.SNR(self)[1]
        
        return avr / len(self.con)

    def show(self, screen, font) :

        if self.p.z > 0 :
           pygame.draw.circle(screen, (0, 0 ,255), [self.p.x+50, self.p.y+50], 5)
        else :
            pygame.draw.circle(screen, (255, 255, 255), [self.p.x+50, self.p.y+50], 5)
        

        f = font.render(str(int(self.p.z)), 1, pygame.Color("coral"))
        screen.blit(f, (self.p.x-10,self.p.y+50))

        f1 = font.render(str(int(self.n_users)), 1, pygame.Color("coral"))
        screen.blit(f1, (self.p.x+60,self.p.y+50))


    def EnergyConsumption(self, v) :

        p0 = 577.3  # Watt   ---> Blade profile power
        pi = 793.0  # Watt   ---> induced power
        Utip = 200  # m/s    ---> tip speed of the rotor blade
        v0 = 7.21   # m/s    ---> the mean rotor induced velocity in hover
        d0 = 0.3    #        ---> fusilage drag ratio
        rho = 1.225 # kg/m3  ---> Air density
        s = 0.05    #        ---> rotor solidity
        A = 0.79    # m2     ---> rotor disk area

        p = p0 * (1 + (3* v**2 / Utip**2)) + pi * (np.sqrt(1+(v**4/4*v0**4))-(v**2/2*v0**2))**(1/2) + 1/2*d0*rho*s*A*v**3

        return p