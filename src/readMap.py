import pygame

def read() :
    obs = []
    i, j = 0, 0
    f = open("src\map", 'r')
    
    for line in f :
        for c in line :
            if c == 'X' :
                for n in range(10) :
                    obs.append([pygame.Vector3(i, j, n*10), [32, 32]])
            i += 32
        i = 0
        j += 32
        
    f.close()
    return obs

def draw(screen, wall, obs):

    for ob in obs :
        screen.blit(wall, (ob[0].x,ob[0].y))

    