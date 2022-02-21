import random
import numpy as np
import sys

from math import acos, asin, cos, degrees, sqrt
from random import shuffle
from tabulate import tabulate



import sys
sys.path.append('..')

from src.neurovec3D import NeuroVector3D


DEFAULT_RESOLUTION = 3600

def extract(x, y, z):
    ro = sqrt(x*x+y*y+z*z)

    if ro == 0:
        return [0, 0, 0]

    phi   = asin(z / ro)
    theta = asin(y / (ro * cos(phi)))

    return [theta, phi, ro]
    
if __name__ == '__main__':
    name, *args = sys.argv
    nums = int(args[0])
    resolution = int(args[1]) if len(args) > 1 else DEFAULT_RESOLUTION

    # a = np.array([0.505421, 0.336309, 0.757456])
    # b = np.ones(3) + a
    # print(degrees(acos(a.dot(b)/(np.linalg.norm(a) * np.linalg.norm(b)))))

    np.random.seed(5)
    random.seed(5)

    test_samples  = np.random.random((nums, 3))*100
    test_samples2 = test_samples.copy()
    lambda_samples= np.random.random(nums)

    shuffle(test_samples2)

    test_neovecs         = np.array([*map(lambda x:NeuroVector3D.fromCartesianVector(*x,resolution), test_samples ),])
    test_neovecs2        = np.array([*map(lambda x:NeuroVector3D.fromCartesianVector(*x,resolution), test_samples2),])

    addition_samples     = test_samples + test_samples2
    addition_neovecs     = test_neovecs + test_neovecs2
    addition_neovecs     = np.array([*map(NeuroVector3D.extractCartesianParameters, addition_neovecs     ),])
    #addition_samples     = np.array([*map(lambda x:extract(*x), addition_samples     ),])

    substraction_samples = test_samples - test_samples2
    substraction_neovecs = test_neovecs - test_neovecs2
    substraction_neovecs = np.array([*map(NeuroVector3D.extractCartesianParameters, substraction_neovecs ),])
    #substraction_samples = np.array([*map(lambda x:extract(*x), substraction_samples ),])

    #multiplitaion_samples= (test_samples * np.dstack((lambda_samples, lambda_samples, lambda_samples)))[0]

    #multiplitaion_neovecs= test_neovecs * lambda_samples

    #multiplitaion_neovecs= np.array([*map(NeuroVector3D.extractPolarParameters, multiplitaion_neovecs),])

    #multiplitaion_samples= np.array([*map(lambda x:extract(*x), multiplitaion_samples),])

    vnorm   = np.linalg.norm(substraction_samples, axis=1)
    neonorm = np.linalg.norm(substraction_neovecs, axis=1)
    v       = vnorm * neonorm

    dot = (substraction_samples * substraction_neovecs).sum(axis=1)
    print(np.degrees(np.arccos(dot / v)))
    exit()

    addition_error      = sum(np.abs(addition_neovecs      - addition_samples     )) / nums
    #substraction_error  = sum(np.abs(substraction_neovecs  - substraction_samples )) / nums
    #multiplitaion_error = sum(np.abs(multiplitaion_neovecs - multiplitaion_samples)) / nums


    #addition_error     [0] = np.degrees(addition_error     [0])
    #substraction_error [0] = np.degrees(substraction_error [0])
    #multiplitaion_error[0] = np.degrees(multiplitaion_error[0])

    #addition_error     [1] = np.degrees(addition_error     [1])
    #substraction_error [1] = np.degrees(substraction_error [1])
    #multiplitaion_error[1] = np.degrees(multiplitaion_error[1])


    print(
        tabulate([
            ["Addition"] + list(addition_error),
            #["Substraction"] + list(substraction_error),
            #["Multiplication"] + list(multiplitaion_error)
            ], headers=["Operation", "Theta error in deg°", "Phi error in deg°", "Length error"]))