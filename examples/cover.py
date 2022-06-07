from asyncio.windows_events import NULL
import glm
from drone import Drone


def average_SNR(users) :

        avr = 0

        for user in users :
            if user.isConnected != NULL : avr += user.SNR(user.isConnected)[1]

        return avr / len(users)

def clear(users, drones) :

    for user in users :
        user.isConnected = NULL

    for drone in drones :
        drone.n_users = 0
        drone.connected_users.clear()
    

def reArrange(users, drones, T) :

    clear(users, drones)
    non_con = len(users)

    for drone in drones :

        snr_list = []
        for user in users :
            if user.isConnected == NULL :
                snr = user.SNR(drone)[0]
                #snr = glm.length(user.position - drone.position)

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


def update(drones, users, non_con_tr, app, T) :

    non_con = reArrange(users, drones, T)

    stable = True
    for drone in drones :

        F = drone.force(users, drones, non_con)
        if glm.length(F) > 0.005 :
            stable = False

        dt = glm.normalize(F) * 0.1
        drone.position += dt
        drone.obj.m_Position = drone.position
        drone.coneObj.m_Position = drone.position - glm.vec3(0, drone.position.y, 0)

    if stable == True :

        n_p = non_con * 100 / len(users)

        if n_p > non_con_tr :

            d = Drone(app)
            drones.insert(0, d)
            stable = False
    
    return non_con
    