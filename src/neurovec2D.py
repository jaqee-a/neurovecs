from math import atan2, cos, sin, sqrt
import numpy as np


class NeuroVector2D:

    __SWV     : np.ndarray
    bias      :float
    resolution: int

    @staticmethod
    def fromCartesianVector(x: float, y: float, resolution: int):
        rho   = sqrt(x*x+y*y)
        theta = atan2(y, x)

        return NeuroVector2D(rho=rho, theta=theta, resolution=resolution)

    @staticmethod
    def fromSWV(swv: np.ndarray, bias: float):
        out = NeuroVector2D(swv=swv)

        out.bias = bias

        return out

    def __init__(self, rho: float = None, theta: float = None, resolution: int = None, swv: np.ndarray = None) -> None:

        if type(swv) == np.ndarray:
            self.resolution = swv.size
            self.__SWV = swv
        else:
            assert rho != None and theta != None and resolution != None, "You must provide either 'SWV' or (rho, theta and resolution) in the constructor"
            
            self.resolution = resolution

            self.__SWV = np.zeros(self.resolution)

            self.bias = 0
            self.calculateSineWaveVector(rho, theta)

    def calculateSineWaveVector(self, rho: float, theta: float):
        space = np.linspace(-np.pi, np.pi, self.resolution, endpoint=False)

        self.__SWV = rho * np.cos(space - theta)

        min_val = self.__SWV.min()

        if min_val < 0:
            self.bias = abs(min_val)

            self.__SWV += self.bias


    def extractPolarParameters(self):
        argmax_ = np.argmax(self.__SWV)

        rho     = self.__SWV[argmax_] - self.bias
        #                                       #This basically means if rho == 0 theta is also 0
        theta   = ((argmax_*np.pi*2/self.resolution)-np.pi) * (rho != 0)

        return theta, rho

    def extractCartesianParameters(self):
        theta, rho = self.extractPolarParameters()

        x = rho * cos(theta)
        y = rho * sin(theta)

        return x, y

    def getSWV(self):
        return self.__SWV

    def __sub__(self, __o):
        assert self.__SWV.size == __o.__SWV.size, "SUB: Unmatched resolution"
        assert type(__o) == NeuroVector2D,        "SUB: Wrong second-hand type"


        """
            By subtraction we can invert the second-hand Sine Wave function and doing the addition
            Inverting a Sine Wave function is same as offsetting the input by pi
        
        """

        return self + (~__o)


    def __add__(self, __o):
        assert self.__SWV.size == __o.__SWV.size, "ADD: Unmatched resolution"
        assert type(__o) == NeuroVector2D,        "ADD: Wrong second-hand type"

        return NeuroVector2D.fromSWV(self.__SWV + __o.__SWV, self.bias + __o.bias)


    def __invert__(self):
        vm    = self.__SWV.copy()
        min__ = vm.min()
        max__ = vm.max() - min__
        vm    = max__ - (vm - min__) + min__

        return NeuroVector2D.fromSWV(vm, self.bias)

    def __mul__(self, __o):
        assert type(__o) == int or type(__o) == float or type(__o) == NeuroVector2D, "MUL:Wrong second-hand type"

        if type(__o) == NeuroVector2D:
            argmax_ = np.argmax(self.__SWV)

            return (self.__SWV[argmax_] - self.bias) * (__o.__SWV[argmax_] - __o.bias)


        # INVERT THE MATRIX
        vm = self.__SWV.copy()
        if __o < 0:
            min__ = vm.min()
            max__ = vm.max() - min__
            vm = max__ - (vm - min__) + min__
            __o   = abs(__o)

        return NeuroVector2D.fromSWV(vm * __o, self.bias * __o)

