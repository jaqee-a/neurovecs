import glm

from core.components.mesh import Mesh
from drone import Drone
import core.time
from simulation.imguiapp import ImGuiApp


    
nonConnectedColor = glm.vec4(0 , 0, 0, 1.0)


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
                snr = user.SNR(drone)[0]

                if snr >= T :
                   snr_list.append([snr, user])

        snr_list.sort(reverse = True, key = lambda x:x[0])
        i = 0
        
        while i < Drone.capacity and i < len(snr_list) :
            snr_list[i][1].isConnected = drone
            non_con -= 1
            drone.n_users += 1
            drone.connected_users.append(snr_list[i][1])
            i += 1

    return non_con


def update(drones, users, T, obstacles) :
    non_con = reArrange(users, drones, T)

    for drone in drones :

        F = drone.force(users, drones, non_con, obstacles)
        
        dt = glm.normalize(F) 
        drone.position += dt
        drone.obj.getComponent(core.components.transform.Transform).m_Position = drone.position
        
        
    
    for user in users:
        uMesh = user.obj.getComponent(core.components.transform.Transform).m_Entity.getComponent(Mesh)

        if user.isConnected: 
            uMesh.m_BlendColor = user.isConnected.color
        else :
            uMesh.m_BlendColor = nonConnectedColor

    return non_con
    