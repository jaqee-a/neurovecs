from random import random
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('..')

from src.neurovec2D import NeuroVector2D

RES = 250


if __name__ == '__main__':
    vec1 = np.array([random()*44 - 22, random()*44 - 22])

    nvec1 = NeuroVector2D.fromCartesianVector(*vec1, RES)
    theta, rho = NeuroVector2D.extractPolarParameters(nvec1)
    nvec2 = NeuroVector2D.fromSWV((rho + nvec1.bias) - nvec1.getSWV(), nvec1.bias)
    nvec3 = nvec1 - nvec1

    vec2 = nvec2.extractCartesianParameters()

    x = np.linspace(-np.pi, np.pi, RES, endpoint=True)

    y1 = nvec1.getSWV()
    y2 = nvec2.getSWV()


    fig, axis = plt.subplots(3, 2)

    axis[0, 0].plot(x, y1)
    axis[1, 0].plot(x, y2)
    axis[2, 0].plot(x, nvec3.getSWV())
    
    axis[0, 1].arrow(0, 0, *vec1, head_width=0, head_length=0, fc='lightblue', ec='black')
    axis[1, 1].arrow(0, 0, *vec2, head_width=0, head_length=0, fc='lightblue', ec='black')

    xs = np.array([vec1[0], vec2[0]])
    ys = np.array([vec1[1], vec2[1]])

    minx = max(*xs, *(-xs)) + 10
    miny = max(*ys, *(-ys)) + 10

    axis[0, 1].set_ylim([-miny, miny])
    axis[1, 1].set_ylim([-miny, miny])

    axis[0, 1].set_xlim([-minx, minx])
    axis[1, 1].set_xlim([-minx, minx])
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
