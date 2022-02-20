from math import degrees
from random import random
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('..')

from src.neurovec3D import NeuroVector2D

RES = 250


if __name__ == '__main__':
    vec1 = np.array([random()*44 - 22, random()*44 - 22])    
    vec2 = np.array([random()*44 - 22, random()*44 - 22])
    #vec1 = [20, 40]
    #vec2 = [-20, 40]

    nvec1 = NeuroVector2D.fromVector(*vec1, RES)
    nvec2 = NeuroVector2D.fromVector(*vec2, RES)

    nvec3 = nvec1 - nvec2

    x  = (np.arange(RES+1)*2*np.pi/RES+1)-np.pi

    y1 = nvec1.getVS()
    y2 = nvec2.getVS()
    y3 = nvec3.getVS()

    fig, axis = plt.subplots(3, 2)

    axis[0, 0].plot(x, y1)
    axis[1, 0].plot(x, y2)
    axis[2, 0].plot(x, y3)

    ymax = y3.max()
    ymin = y3.min()

    axis[0, 0].set_ylim([ymin - 50, ymax + 50])
    axis[1, 0].set_ylim([ymin - 50, ymax + 50])
    axis[2, 0].set_ylim([ymin - 50, ymax + 50])

    vec3 = nvec3.toVec()
    

    res = NeuroVector2D.fromVector(*(vec1 - vec2), RES)

    print(nvec3.theta, degrees(nvec3.theta))
    print(res.theta, degrees(res.theta))

    axis[0, 1].arrow(0, 0, *vec1, head_width=0, head_length=0, fc='lightblue', ec='black')
    axis[1, 1].arrow(0, 0, *vec2, head_width=0, head_length=0, fc='lightblue', ec='black')


    axis[2, 1].arrow(0, 0, *vec3, head_width=0, head_length=0, fc='lightblue', ec='black')
    axis[2, 1].arrow(0, 0, *vec1, head_width=0, head_length=0, fc='lightblue', ec='black')
    axis[2, 1].arrow(*vec1, *(-vec2), head_width=0, head_length=0, fc='lightblue', ec='black')

    xs = np.array([vec1[0], vec2[0], vec3[0]])
    ys = np.array([vec1[1], vec2[1], vec3[1]])

    minx = max(*xs, *(-xs)) + 10
    miny = max(*ys, *(-ys)) + 10

    axis[0, 1].set_ylim([-miny, miny])
    axis[1, 1].set_ylim([-miny, miny])
    axis[2, 1].set_ylim([-miny, miny])

    axis[0, 1].set_xlim([-minx, minx])
    axis[1, 1].set_xlim([-minx, minx])
    axis[2, 1].set_xlim([-minx, minx])
    fig.set_facecolor('lightsteelblue')

    """
    print(x, y1)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.xcorr(x, y1, maxlags=4)
    ax1.grid(True)
    ax1.axhline(0, color='black')
    
    #ax2 = fig.add_subplot(212, sharex=ax1)
    #ax2.acorr(x, usevlines=True, normed=True, maxlags=4, lw=2)
    #ax2.grid(True)
    #ax2.axhline(0, color='black', lw=2)

    """
    plt.show()
