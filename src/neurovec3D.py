# PHI  == ELEVATION
# THETA== AZIMUTH

from math import atan2, cos, sin, sqrt
import numpy as np


class NeuroVector3D:

    __MS      : np.ndarray
    bias      : float
    resolution: int


    @staticmethod
    def fromCartesianVector(x: float, y: float, z: float, resolution: int):
        rho   = sqrt(x*x+y*y+z*z)

        phi   = 0
        theta = 0

        if rho != 0:        
            theta = atan2(y, x)
            phi   = np.pi / 2 - atan2(sqrt(x*x+y*y), z)

        #print(phi, theta)
        return NeuroVector3D(rho=rho, theta=theta, phi=phi, resolution=resolution)

    # TODO TEST!
    @staticmethod
    def fromMS(ms: np.ndarray, bias = None):
        out = NeuroVector3D(ms=ms)

        if bias == None:
            min_val = ms.min()
            out.bias = 0
            if min_val < 0:
                out.bias = abs(min_val)
            if min_val < 50:
                out.bias += 50
            out.__MS += out.bias
        else:
            out.bias = bias
        
        
        return out

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

    def calculateSineWaveVector(self, rho: float, theta: float, phi: float):

        elevation = np.linspace(-np.pi/2, np.pi/2, self.resolution, endpoint=True)
        azimuth   = np.linspace(-np.pi, np.pi, self.resolution, endpoint=False)

        ones   = np.ones((self.resolution, self.resolution))

        phis   = (elevation * ones).T
        thetas =    azimuth * ones

        #ρ0(cosδ cosδ0 cos(θ − θ0) + sinδ sinδ0)
        self.__MS = rho * (cos(phi) * np.cos(phis) * np.cos(thetas - theta) + sin(phi) * np.sin(phis))

        min_val = self.__MS.min()
        
        if min_val < 0:
            self.bias = abs(min_val) + 50

            self.__MS += self.bias


    # TODO TEST!
    def extractPolarParameters(self):
        #argmax_ = np.argmax(self.__MS)
        max_element = self.__MS.max()

        xs, ys = np.where(self.__MS == max_element)
        x, y = xs[0], ys[0]

        rho     = max_element - self.bias
        #                                       #This basically means if ro == 0 theta is also 0
        theta = (-np.pi     + ((y*np.pi*2/(self.resolution))))   * (rho != 0)
        phi   = (-np.pi / 2 + ((x*np.pi  /(self.resolution-1)))) * (rho != 0)

        return theta, phi, rho

    def extractCartesianParameters(self):
        theta, phi, rho = self.extractPolarParameters()

        x = rho * cos(phi) * cos(theta)
        y = rho * cos(phi) * sin(theta)
        z = rho * sin(phi)

        return x, y, z

    def getMS(self):
        return self.__MS
        
    def __sub__(self, __o):
        assert self.__MS.shape == __o.__MS.shape, "SUB: Unmatched resolution"
        assert type(__o) == NeuroVector3D,        "SUB: Wrong second-hand type"


        """
            By subtraction we can invert the second-hand Sine Wave function and doing the addition
            Inverting a Sine Wave function is same as offsetting the input by pi
        """

        return self + (~__o)


    def __invert__(self):
        vm    = self.__MS.copy()
        min__ = vm.min()
        max__ = vm.max() - min__
        vm    = max__ - (vm - min__) + min__

        return NeuroVector3D.fromMS(vm, self.bias)

    # TODO  TEST!
    def __add__(self, __o):
        assert self.__MS.shape == __o.__MS.shape, "ADD: Unmatched resolution"
        assert type(__o) == NeuroVector3D,        "ADD: Wrong second-hand type"

        return NeuroVector3D.fromMS(self.__MS + __o.__MS, self.bias + __o.bias)


    # TODO TEST!
    def __mul__(self, __o):
        assert type(__o) == int or type(__o) == float or type(__o) == NeuroVector3D, "MUL: Wrong second-hand type"

        if type(__o) == NeuroVector3D:
            xs, ys = np.where(self.__MS == self.__MS.max())
            x, y = xs[0], ys[0]

            return (self.__MS[x, y] - self.bias) * (__o.__MS[x, y] - __o.bias)


        # INVERT THE VECTOR
        vm = self.__MS.copy()

        if __o < 0:
            min__ = vm.min()
            max__ = vm.max() - min__
            vm    = max__    - ( vm - min__ ) + min__
            __o   = abs(__o)

        return NeuroVector3D.fromMS((vm - self.bias) * __o)

    def __normalize__(self):

            vm    = self.__MS.copy()
            max__ = vm.max() - self.bias
            vm    = vm.__mul__(1 / max__)

            return NeuroVector3D.fromMS(vm, self.bias / max__)
        