"""
    TODO WHAT CAN I DO ?

    -   Create a cartesian vector, polar vector from the sine wave
    -   Create a sine wave, polar vector from the cartesian vector


        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
        |------------------------------------------------------------|
"""




from math import asin, cos, sin, sqrt
from time import time
import numpy as np


class NeuroVector3D:

    __MS      : np.ndarray
    bias      : float
    resolution: int


    # TODO TEST
    @staticmethod
    def fromCartesianVector(x: float, y: float, z: float, resolution: int):
        rho    = sqrt(x*x+y*y+z*z)
        phi   = asin(z / rho)
        theta = asin(y / (rho * cos(phi)))

        return NeuroVector3D(rho=rho, theta=theta, phi=phi, resolution=resolution)

    # TODO TEST!
    @staticmethod
    def fromMS(ms: np.ndarray, bias: float):
        out = NeuroVector3D(ms=ms)

        out.bias = bias

        return out

    # TODO TEST!
    def __init__(self, rho: float = None, theta: float = None, phi: float = None, resolution: int = None, ms: np.ndarray = None) -> None:

        if type(ms) == np.ndarray:
            self.resolution = ms.shape[0]
            self.__MS = ms
        else:
            assert rho != None and theta != None and resolution != None and phi != None, "You must provide either 'MS' or (rho, theta, phi and resolution) in the constructor"
            
            self.resolution = resolution

            self.__MS = np.zeros((self.resolution, self.resolution))

            self.bias = 0
            self.calculateSineWaveVector(rho, theta, phi)

    # TODO TEST!
    def calculateSineWaveVector(self, rho: float, theta: float, phi: float):

        space  = np.linspace(-np.pi, np.pi, self.resolution, endpoint=True)
        ones   = np.ones((self.resolution, self.resolution))

        thetas = space*ones
        phis   = thetas.T

        #ρ0(cosδ cosδ0 cos(θ − θ0) + sinδ sinδ0)
        self.__MS = rho * (cos(phi) * np.cos(phis) * np.cos(thetas - theta) + sin(phi) * np.sin(phis))

        min_val = self.__MS.min()
        
        if min_val < 0:
            self.bias = abs(min_val)

            self.__MS += self.bias


    # TODO TEST!
    def extractPolarParameters(self):
        #argmax_ = np.argmax(self.__MS)
        max_element = self.__MS.max()

        xs, ys = np.where(self.__MS == max_element)
        x, y = ys[0], xs[0]

        rho     = max_element - self.bias
        #                                       #This basically means if ro == 0 theta is also 0
        theta   = ((x*np.pi*2/self.resolution)-np.pi) * (rho != 0)
        phi     = ((y*np.pi*2/self.resolution)-np.pi) * (rho != 0)

        return theta, phi, rho

    # TODO TEST!
    def extractCartesianParameters(self):
        theta, phi, rho = self.extractPolarParameters()


        x = rho * cos(phi) * cos(theta)
        y = rho * cos(phi) * sin(theta)
        z = rho * sin(phi)

        return x, y, z

    def getMS(self):
        return self.__MS
        
    # TODO TEST!
    def __sub__(self, __o):
        assert self.__MS.shape == __o.__MS.shape, "SUB: Unmatched resolution"
        assert type(__o) == NeuroVector3D,        "SUB: Wrong second-hand type"


        """
            By subtraction we can invert the second-hand Sine Wave function and doing the addition
            Inverting a Sine Wave function is same as offsetting the input by pi
            
            Slide the array by N / 2, as N represents 2*pi, N / 2 represents pi.
        
        TODO
            Check why this method has more error rate on the angle
        
        """
        max_ = __o.__MS.max()
        new_vs = max_ - __o.__MS

        return NeuroVector3D.fromMS(self.__MS + new_vs, self.bias + __o.bias)


    # TODO  TEST!
    def __add__(self, __o):
        assert self.__MS.shape == __o.__MS.shape, "ADD: Unmatched resolution"
        assert type(__o) == NeuroVector3D,        "ADD: Wrong second-hand type"

        return NeuroVector3D.fromMS(self.__MS + __o.__MS, self.bias + __o.bias)


    # TODO TEST!
    def __mul__(self, __o):
        assert type(__o) == int or type(__o) == float or type(__o) == NeuroVector3D, "MUL: Wrong second-hand type"

        if type(__o) == NeuroVector3D:
            return NeuroVector3D.fromMS(self.__MS * __o.__MS, self.bias * __o.bias)

        return NeuroVector3D.fromMS(self.__MS * __o, abs(self.bias * __o))

