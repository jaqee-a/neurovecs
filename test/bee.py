import pygame
import random
import numpy as np
import sys

from math import asin, cos, degrees, sqrt
from tabulate import tabulate



import sys
sys.path.append('..')

from src.neurovec2D import NeuroVector2D


def getDT(pp, pc, p0):
    rf = np.array([0, 0])
    rpp = np.array([0, 0])

    rf[0] = pp[0] - p0[0]
    rf[1] = pp[1] - p0[1]

    rpp[0] = pc[0] - pp[0]
    rpp[1] = pc[1] - pp[1]

    rpp[0] *= l
    rpp[1] *= l

    rf[0] *= (l - 1)
    rf[1] *= (l - 1)

    return rpp + rf


resolution = 4

nrefp  = NeuroVector2D.fromCartesianVector(0, 0, resolution)
nrp    = NeuroVector2D.fromCartesianVector(0, 0, resolution)
npp    = NeuroVector2D.fromCartesianVector(300, 0, resolution)

nup    = NeuroVector2D.fromCartesianVector(0, 1, resolution)

proie = [50, 0, 25, 25]
pret  = [250, 0, 25, 25]

l = 0
rp = np.array([0, 0])
refp = np.array([0, 0])
pp = np.array([300, 0])
a = .016

pygame.init()
pygame.mixer.init()
running = True
image = pygame.Surface((400, 400))
delta_time = 0
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
start = False
while running:
    image.fill((175, 255, 175))
    delta_time = clock.tick(30) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start = True

    if not start: continue
    
    pygame.draw.rect(image, (255, 0, 0), proie)
    
    pygame.draw.rect(image, (0, 0, 255), pret)


    refp = NeuroVector2D.fromCartesianVector(*(pret[:2]), resolution) - npp


    rp   = NeuroVector2D.fromCartesianVector(*(proie[:2]), resolution) - NeuroVector2D.fromCartesianVector(*(pret[:2]), resolution)

    rpl  = rp * l
    refpl = refp * (l-1)

    ndt = rpl + refpl

    xx, yy = getDT(pret, proie, pp)


    l += a * (1 - l)

    x, y = ndt.extractCartesianParameters()

    print(*np.round(np.array([x, y])))

    pret[0] += x
    pret[1] += y

    print(pret)
    
    proie[1] += 1

    screen.blit(pygame.transform.flip(image, False, True), (0, 0))
    pygame.display.flip()
pygame.quit()