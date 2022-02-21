from math import atan2, cos, sin, sqrt
import numpy as np



class NeuroVector2D:

    __VS : np.ndarray
    bias : float
    theta: float
    ro   : float
    res  : int

    @staticmethod
    def fromVS(vs: np.ndarray, bias: float):
        max_  = np.argmax(vs)
        
        ro    = vs[max_] - bias
        
        #                                       #This basically means if ro == 0 theta is also 0
        theta = ((max_*2*np.pi/vs.size)-np.pi) * (ro != 0)

        out   = NeuroVector2D(ro, theta, vs.size, False)

        out.setVS(vs, bias)

        return out

    @staticmethod
    def fromVector(x: float, y: float, res: int):
        return NeuroVector2D(sqrt(x*x+y*y), atan2(y, x), res)

    def __init__(self, ro: float, theta: float, res: int, calcVS: bool = True) -> None:
        self.theta = theta
        self.ro    = ro
        self.res   = res

        self.bias = 0
        self.__VS = np.zeros(self.res)

        if calcVS: self.calculateVS()

    def calculateVS(self):
        #space = np.linspace(-np.pi, np.pi, self.res, endpoint=True)
        space = (np.arange(self.res+1)*2*np.pi/self.res)-np.pi
        self.setVS(self.ro * np.cos(space - self.theta), None)
        
    def getVS(self):
        return self.__VS

    def setVS(self, VS: np.ndarray, bias: float):
        self.__VS = VS
        if bias == None:
            self.bias = abs(min(VS.min(), 0))
            self.__VS += self.bias
        else:
            self.bias = bias

    def toVec(self):
        return self.ro * cos(self.theta), self.ro * sin(self.theta)

    def getValues(self):
        return [self.theta, self.ro]

    def __sub__(self, __o):
        assert self.__VS.size == __o.__VS.size, "SUB: Unmatched resolution"
        assert type(__o) == NeuroVector2D, "SUB: Wrong second-hand type"


        """
            By subtraction we can invert the second-hand Sine Wave function and doing the addition
            Inverting a Sine Wave function is same as offsetting the input by pi
            
            Slide the array by N / 2, as N represents 2*pi, N / 2 represents pi.
            new_vs = np.roll(__o.__VS, __o.res // 2)
        """

        """ TODO
            Check why this method has more error rate on the angle
        """ 
        return NeuroVector2D.fromVS(self.__VS - __o.__VS, self.bias - __o.bias)


    def __add__(self, __o):
        assert self.__VS.size == __o.__VS.size, "ADD:Unmatched resolution"
        assert type(__o) == NeuroVector2D, "ADD: Wrong second-hand type"

        return NeuroVector2D.fromVS(self.__VS + __o.__VS, self.bias + __o.bias)


    def __mul__(self, __o):
        assert type(__o) == int or type(__o) == float or type(__o) == NeuroVector2D, "MUL:Wrong second-hand type"

        if type(__o) == NeuroVector2D:
            return NeuroVector2D.fromVS(self.__VS * __o.__VS, self.bias * __o.bias)

        return NeuroVector2D.fromVS(self.__VS * __o, abs(self.bias * __o))


