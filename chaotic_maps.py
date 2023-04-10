from math import sin, cos, pi
import numpy as np

class ChaoticMap:
    '''
    Represents a ChaoticMap
    '''
    def __init__(
        self,
        x0: float,
        y0: float,
        a: float = 0,
        b: float = 0,
        c: float = 0,
        d: float = 0
    ) -> None:
        '''
        Initialize a Chaotic Map. Origin point coordinates
        are required to be specified.
        Up to 4 chaotic map constants can be specified.
        If they are not, system constnats default to 0.

        :param x0: float origin point x value
        :param y0: float origin point y value
        :param a: float constant 
        :param b: float constant 
        :param c: float constant 
        :param d: float constant 
        
        '''
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.reset_origin(x0, y0)

    def calculate(self, i: int) -> None:
        '''
        Caclculate next values of i^th iteration.
        Add the new values to the lists of xs and ys.

        :param i: int interation index
        '''
        x = self.xs[i]
        y = self.ys[i]
        x_new, y_new = self.step(x, y)
        self.xs.append(x_new)
        self.ys.append(y_new)

    def step(self, x, y):
        '''
        Perform calculations with given x and y.

        :param x: float x value
        :param y: float y value
        '''
        return x,y 
    def reset_origin(self, x0, y0) -> None:
        '''
        Reset map to a specified origin (x0, y0)

        :param x0: float origin point x value
        :param y0: float origin point y value
        '''
        self.xs = [x0]
        self.ys = [y0]
    def get_points(self):
        '''
        Return lists of points for x and y axis
        of the the chaotic map.
        '''
        return self.xs, self.ys


class Simulator:
    '''
    Represents a simulator that runs
    calculations for a given chaotic map.
    '''
    def __init__(self, chaotic_map: ChaoticMap, iter_n: int) -> None:
        '''
        Initialize a simulator. An instance of 
        a chaotic map should inherit from the abstract class
        Chaotic Map.

        :param chaotic_map: instance inheriting from the abstract ChaoticMap class
        :param iter_n: int number of iterations for simulation
        '''
        self.chaotic_map = chaotic_map
        self.iter_n = iter_n
    def simulate(self) -> None:
        '''
        Calculate lists of points for x and y axis
        of the chaotic map.
        Returns lists of points for x and y axis
        of the the chaotic map.
        '''
        for i in range(self.iter_n):
            self.chaotic_map.calculate(i)
        return self.chaotic_map.get_points()
    def simulate_in_range(self, x0, x1, y0, y1, step):
        '''
        Calclulate lists of points for x and y axis
        of the chaotic map.
        Creates a generator. Yields lists of points for x and y axis
        of the the chaotic map.

        :param x0: float starting x point
        :param x1: float last x point
        :param y0: float starting y point
        :param y1: float last y point
        :param step: float step of the simulation.
        '''
        for x in np.arange(x0, x1, step):
            for y in np.arange(y0, y1, step):
                self.chaotic_map.reset_origin(x, y)
                xs, ys = self.simulate()
                yield xs, ys
                
    def change_chaotic_map(self, chaotic_map: ChaoticMap):
        '''
        Change current chaotic map to a given one.

        :param chaotic_map: instance inheriting from the abstract ChaoticMap class
        '''
        self.chaotic_map = chaotic_map
    def change_iter_n(self, iter_n: int):
        '''
        Change current number of iterations for simulation to a given one.

        :param iter_n: int number of iterations for simulation
        '''
        self.iter_n = iter_n
    

class TinkerbellMap(ChaoticMap):
    '''
    Represents a ChaoticMap
    '''
    def __init__(
        self,
        a: float,
        b: float,
        c: float,
        d: float,
        x0: float = 0.1,
        y0: float = 0.1
    ) -> None:
        '''
        Initialize a Tinkerbell Map System.
        The a, b, c, d constants can be specified.
        If not, they default to 0.
        The starting x and y coordinates can be specified.
        If they are not, the system defaults to (0.1, 0.1).

        :param a: float constant 
        :param b: float constant 
        :param c: float constant 
        :param d: float constant
        :param x0: float origin point x value
        :param y0: float origin point y value
        
        '''
        super().__init__(x0, y0, a, b, c, d)

    def step(self, x, y):
        '''
        Perform calculations with given x and y.

        :param x: float x value
        :param y: float y value
        '''
        x_new = x**2 - y**2 + self.a*x + self.b*y
        y_new = 2*x*y + self.c*x + self.d*y
        return x_new, y_new 
    

class BogdanovMap(ChaoticMap):
    '''
    Represents a BogdanovMap
    '''
    def __init__(
        self,
        a: float,
        b: float,
        c: float,
        x0: float = 0.1,
        y0: float = 0.1
    ) -> None:
        '''
        Initialize a Bogdanov Map System.
        The a, b, cconstants can be specified.
        If not, they default to 0.
        The starting x and y coordinates can be specified.
        If they are not, the system defaults to (0.1, 0.1).

        :param a: float constant 
        :param b: float constant 
        :param c: float constant 
        :param x0: float origin point x value
        :param y0: float origin point y value
        
        '''
        super().__init__(x0, y0, a, b, c)

    def step(self,x,y):
        y_new = y*(1+self.a+self.c*x) + self.b*x*(x-1)
        x_new = x+y_new
        return x_new, y_new 

class IkedaMap(ChaoticMap):
    '''
    Represents an Ikeada Map
    '''
    def __init__(
        self,
        a: float,
        x0: float = 2,
        y0: float = 2
    ) -> None:
        '''
        Initialize an Ikeda Map System.
        The a constant can be specified.
        If not, it defaults to 0.
        The starting x and y coordinates can be specified.
        If they are not, the system defaults to (2, 2).

        :param a: float constant 
        :param x0: float origin point x value
        :param y0: float origin point y value
        
        '''
        super().__init__(x0, y0, a)

    def step(self,x,y):
        t = 0.4 - 6/(1+x**2+y**2)
        x_new = 1 + self.a * (x*cos(t) - y*sin(t))
        y_new = self.a * (x*sin(t) + y*cos(t))
        return x_new, y_new

class GingerbreadMap(ChaoticMap):
    '''
    Represents a Gingerbread Map
    '''
    def __init__(
        self,
        x0: float = 1,
        y0: float = 2
    ) -> None:
        '''
        Initialize a Gingerbread Map System.
        The starting x and y coordinates can be specified.
        If they are not, the system defaults to (0, 0).

        :param a: float constant 
        :param x0: float origin point x value
        :param y0: float origin point y value
        
        '''
        super().__init__(x0, y0)

    def step(self,x,y):
        x_new = 1 - y + abs(x)
        y_new = x
        return x_new, y_new

class StandardMap(ChaoticMap):
    '''
    Represents a Standard Map
    '''
    def __init__(
        self,
        a: float,
        x0: float = pi,
        y0: float = pi
    ) -> None:
        '''
        Initialize a Standard Map System.
        The a constant must me specified.
        The starting x and y coordinates can be specified.
        If they are not, the system defaults to (pi, pi).

        :param a: float constant 
        :param x0: float origin point x value
        :param y0: float origin point y value
        
        '''
        super().__init__(x0, y0, a)

    def step(self,x,y):
        x %= (2*pi)

        y_new = y + self.a * sin(x)
        x_new = x + y_new

        return x_new, y_new

