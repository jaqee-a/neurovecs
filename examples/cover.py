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
        user.isConnected = 0

    for drone in drones :
        drone.n_users = 0
        drone.connected_users.clear()

def reArrange(users, drones, T, non_con) :

    clear(users, drones)

    for drone in drones :

        snr_list = []
        for user in users :
            if user.isConnected == NULL and drone.n_users < drone.capacity :
                snr = user.SNR(drone)[0]

                if snr > T :
                   snr_list.append([snr, user])

        snr_list.sort(reverse = True, key = lambda x:x[0])
        i = 0
        while i < drone.capacity and i < len(snr_list) :
            snr_list[i][1].isConnected = drone
            non_con -= 1
            drone.n_users += 1
            drone.connected_users.append(snr_list[i][1])

        return non_con


def update(drones, users, non_con, non_con_tr, app, T) :

    non_con = reArrange(users, drones, T, non_con)
    
    stable = True
    for drone in drones :
        F = drone.force(users, drones, non_con)
        if glm.length(F) > 0.005 :
            stable = False

        dt = F.Normalize() * 0.5
        drone.position += dt
        drone.obj.m_Position = drone.position

    if stable == True :

        n_p = non_con * 100 / len(users)

        if n_p > non_con_tr :

            d = Drone(app)
            drones.insert(0, d)
            stable = False
    
    return non_con
    