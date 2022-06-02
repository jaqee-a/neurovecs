import pygame

def read() :
    obs = []
    i, j = 0, 0
    f = open("src\map", 'r')
    
    for line in f :
        for c in line :
            if c == 'X' :
                for n in range(200) :
                    obs.append([pygame.Vector3(i, j, n), [32, 32]])
            i += 32
        i = 0
        j += 32
        
    f.close()
    return obs

def draw(screen, wall, obs):

    for ob in obs :
        if ob[0].z == 0 :
           screen.blit(wall, (ob[0].x,ob[0].y))

    