import random
import numpy as np
import sys

from math import asin, cos, degrees, sqrt
from tabulate import tabulate



import sys
sys.path.append('..')

from src.neurovec3D import NeuroVector3D


DEFAULT_RESOLUTION = 50

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
    test_samples2 = np.random.random((nums, 3))*100
    lambda_samples= np.random.random(nums)

    test_neovecs         = np.array([*map(lambda x:NeuroVector3D.fromCartesianVector(*x,resolution), test_samples ),])
    test_neovecs2        = np.array([*map(lambda x:NeuroVector3D.fromCartesianVector(*x,resolution), test_samples2),])

    addition_samples     = test_samples + test_samples2
    addition_neovecs     = test_neovecs + test_neovecs2
    addition_neovecs     = np.array([*map(NeuroVector3D.extractCartesianParameters, addition_neovecs     ),])

    substraction_samples = test_samples - test_samples2
    substraction_neovecs = test_neovecs - test_neovecs2
    substraction_neovecs = np.array([*map(NeuroVector3D.extractCartesianParameters, substraction_neovecs ),])

    multiplitaion_samples= (test_samples * np.dstack((lambda_samples, lambda_samples, lambda_samples)))[0]
    multiplitaion_neovecs= test_neovecs * lambda_samples
    multiplitaion_neovecs= np.array([*map(NeuroVector3D.extractCartesianParameters, multiplitaion_neovecs),])

    #multiplitaion_samples= np.array([*map(lambda x:extract(*x), multiplitaion_samples),])

    print(test_samples[0])
    print(test_samples2[0])

    sample1  = addition_samples[0]

    a=NeuroVector3D.fromCartesianVector(1, 2, 3, 5)

    vnorm_sub   = np.linalg.norm(substraction_samples, axis=1)
    neonorm_sub = np.linalg.norm(substraction_neovecs, axis=1)
    v_sub       = vnorm_sub * neonorm_sub

    dot_sub = (substraction_samples * substraction_neovecs).sum(axis=1)
    angle_err_sub = np.degrees(np.arccos(dot_sub / v_sub)).sum() / nums

    vnorm_add   = np.linalg.norm(addition_samples, axis=1)
    neonorm_add = np.linalg.norm(addition_neovecs, axis=1)
    v_add       = vnorm_add * neonorm_add

    dot_add = (addition_samples * addition_neovecs).sum(axis=1)
    angle_err_add = np.degrees(np.arccos(dot_add / v_add)).sum() / nums

    vnorm_mul   = np.linalg.norm(multiplitaion_samples, axis=1)
    neonorm_mul = np.linalg.norm(multiplitaion_neovecs, axis=1)
    v_mul       = vnorm_mul * neonorm_mul

    dot_mul = (multiplitaion_samples * multiplitaion_neovecs).sum(axis=1)
    angle_err_mul = np.degrees(np.arccos(dot_mul / v_mul)).sum() / nums

    #addition_error      = sum(np.abs(addition_neovecs      - addition_samples     )) / nums
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
            ["Addition"] + [np.abs(angle_err_add)],
            ["Substraction"] + [np.abs(angle_err_sub)],
            ["Multiplication"] + [np.abs(angle_err_mul)]
            ], headers=["Operation", "Theta error in deg°", "Phi error in deg°", "Length error"]))