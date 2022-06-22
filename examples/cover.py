import glm

from core.components.mesh import Mesh
from drone import Drone
from user import User
import numpy as np

    
nonConnectedColor = glm.vec4(0.8, 0.3, 0.4, 1.0)
connectedColor = glm.vec4(0.3, 0.8, 0.4, 1.0)


def average_SNR(users) :

        avr = 0

        for user in users :
            if user.isConnected != None : avr += user.SNR(user.isConnected)[1]

        return avr / len(users)

def clear(users, drones) :

    for user in users :
        user.isConnected = None

    for drone in drones :
        drone.n_users = 0
        drone.connected_users.clear()
    

def reArrange(users, drones, T) :

    clear(users, drones)
    non_con = len(users)

    for drone in drones :

        snr_list = []
        for user in users :
            if user.isConnected == None :
                dist = glm.length(drone.position - user.position) #m
                r = np.sqrt(dist**2 - (drone.position.y-1)**2)
                snr = User.SNR(drone, r)[0]

                if snr > T :
                   snr_list.append([snr, user])

        snr_list.sort(reverse = True, key = lambda x:x[0])
        i = 0
        
        while i < Drone.capacity and i < len(snr_list) :
            snr_list[i][1].isConnected = drone
            non_con -= 1
            drone.n_users += 1
            drone.connected_users.append(snr_list[i][1])
            i += 1
            user.obj.m_color = drone.color
        

    return non_con


def update(drones, users, non_con_tr, app, T, droneMesh, obstacles) :

    non_con = reArrange(users, drones, T)

    stable = True
    for drone in drones :

        F = drone.force(users, drones, non_con)
        if glm.length(F) > 0.005 :
            stable = False

        dt = glm.normalize(F) * 0.1
        drone.position += dt
        drone.obj.m_Position = drone.position
        #drone.coneObj.m_Position = drone.position - glm.vec3(0, 20, 0)

    if stable == True :

        n_p = non_con * 100 / len(users)

        if n_p > non_con_tr :

            d = Drone(app, droneMesh, coneMesh, obstacles)
            drones.insert(0, d)
            stable = False
    
    for user in users:
        uMesh = user.obj.m_Entity.getComponent(Mesh)

        if user.isConnected: uMesh.m_BlendColor = user.isConnected.color

    return non_con
    