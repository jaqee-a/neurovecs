import random
import numpy as np
import sys

from math import atan2, sqrt
from random import shuffle
from tabulate import tabulate



import sys
sys.path.append('..')

from src.neurovec2D import NeuroVector2D


DEFAULT_RESOLUTION = 3600

if __name__ == '__main__':
    name, *args = sys.argv
    nums = int(args[0])
    resolution = int(args[1]) if len(args) > 1 else DEFAULT_RESOLUTION

    np.random.seed(5)
    random.seed(5)

    test_samples  = np.random.random((nums, 2))*100
    test_samples2 = np.random.random((nums, 2))*100

    lambda_samples= np.random.random(nums)

    test_neovecs         = np.array([*map(lambda x:NeuroVector2D.fromCartesianVector(*x,resolution), test_samples ),])
    test_neovecs2        = np.array([*map(lambda x:NeuroVector2D.fromCartesianVector(*x,resolution), test_samples2),])

    addition_samples     = test_samples + test_samples2
    substraction_samples = test_samples - test_samples2
    multiplitaion_samples= (test_samples * np.dstack((lambda_samples, lambda_samples)))[0]

    addition_neovecs     = test_neovecs + test_neovecs2
    substraction_neovecs = test_neovecs - test_neovecs2
    multiplitaion_neovecs= test_neovecs * lambda_samples

    addition_neovecs     = np.array([*map(NeuroVector2D.extractPolarParameters, addition_neovecs     ),])
    substraction_neovecs = np.array([*map(NeuroVector2D.extractPolarParameters, substraction_neovecs ),])
    multiplitaion_neovecs= np.array([*map(NeuroVector2D.extractPolarParameters, multiplitaion_neovecs),])

    addition_samples     = np.array([*map(lambda x:[atan2(x[1], x[0]), sqrt(x[1]**2 + x[0]**2)], addition_samples     ),])
    substraction_samples = np.array([*map(lambda x:[atan2(x[1], x[0]), sqrt(x[1]**2 + x[0]**2)], substraction_samples ),])
    multiplitaion_samples= np.array([*map(lambda x:[atan2(x[1], x[0]), sqrt(x[1]**2 + x[0]**2)], multiplitaion_samples),])


    #print(substraction_samples[:,0].min())
    #print(substraction_neovecs[:,0].min())
    #print(substraction_samples[:,0].max())
    #print(substraction_neovecs[:,0].max())

    addition_error      = sum(np.abs(addition_neovecs      - addition_samples     )) / nums
    substraction_error  = sum(np.abs(substraction_neovecs  - substraction_samples )) / nums
    multiplitaion_error = sum(np.abs(multiplitaion_neovecs - multiplitaion_samples)) / nums


    addition_error     [0] = np.degrees(addition_error     [0])
    substraction_error [0] = np.degrees(substraction_error [0])
    multiplitaion_error[0] = np.degrees(multiplitaion_error[0])


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

    """
    addition_neovecs     = np.array([*map(NeuroVector2D.toVec, addition_neovecs     ),])
    substraction_neovecs = np.array([*map(NeuroVector2D.toVec, substraction_neovecs ),])
    multiplitaion_neovecs= np.array([*map(NeuroVector2D.toVec, multiplitaion_neovecs),])

    addition_error       = sum((addition_neovecs      - addition_samples      ))/nums
    substraction_error   = sum((substraction_neovecs  - substraction_samples  ))/nums
    multiplitaion_error  = sum((multiplitaion_neovecs - multiplitaion_samples ))/nums
    
    """
    print(
        tabulate([
            ["Addition"] + list(addition_error) + [angle_err_add],
            ["Substraction"] + list(substraction_error) + [angle_err_sub],
            ["Multiplication"] + list(multiplitaion_error) + [angle_err_mul]], headers=["Operation", "Theta error in deg°", "Length error", "Angle error in deg°"]))