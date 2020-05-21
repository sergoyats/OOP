# 4th task
# speed in km / h, distance in km, mass in t
class Vehicle:
    def __init__(self, route_number, speed, distance):
        self.route_number = route_number
        self.speed = speed
        self.distance = distance
    
    def travel_time(self):
        result = self.distance / self.speed
        return f'Время в пути: {result} ч'


class Train(Vehicle):
    LOCOMOTIVE_MASS = 192
    # разные вагоны имеют разную массу
    def __init__(self, route_number, speed, distance, wagon_mass):
        super().__init__(route_number, speed, distance)
        self.wagon_mass = wagon_mass
    
    def train_mass(self, number_of_wagons):
        result = self.wagon_mass * number_of_wagons + Train.LOCOMOTIVE_MASS
        return f'Масса поезда: {result} т'


class Jet(Vehicle):
    def __init__(self, route_number, speed, distance, flight_altitude):
        super().__init__(route_number, speed, distance)
        self.flight_altitude = flight_altitude
    
    def ascent_time(self):
        result = (self.flight_altitude / (self.speed / 3)) * 60
        # скорость набора высоты реактивных самолётов обычно составляет треть крейсерской
        return f'Время выхода на эшелон: {result} мин'


print('Пассажирский поезд Одесса – Киев "Черноморец":')
chernomorets = Train(106, 80, 650, 50)
print(chernomorets.train_mass(12))
print(chernomorets.travel_time())

print('\nПассажирский самолёт Киев – Одесса "Boeing 737":')
boeing737 = Jet(195, 900, 450, 5.5)
print(boeing737.ascent_time())
print(boeing737.travel_time())



print('')
# 2nd task
class Q:
    def __init__(self, *, to_str='', **params):
        self._params = params
        self._to_str = to_str
    
    def __or__(self, other):
        self._to_str = f'{str(self)} OR {str(other)}'
        return self

    def __and__(self, other):
        self._to_str = f'{str(self)} AND {str(other)}'
        return self

    def __invert__(self):
       self._to_str = f'NOT {str(self)}'
       return self
    
    def __str__(self):
        result = ''
        if self._to_str:
            result = self._to_str
        elif self._params:
            result = [f'{k}={repr(v)}' for k, v in self._params.items()][0]
        return result


filter = Q(first_name='J') | (Q(last_name='G') & ~Q(email='test@gmail.com'))
print(filter)
# filter.__str__()

filter = (Q(first_name='J') | Q(last_name='J')) & ~Q(email='test@gmail.com')
print(filter)



# 3rd task
print('\nЦентр круга в начале координат:')

class Shape1:
    def __init__(self):
        pass


class Point1(Shape1):
    # x, y - координаты точки
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self):
        return self.x ** 2 + self.y ** 2


class Circle1(Shape1):
    def __init__(self, r):
        self.r = r
    
    def belonging(self, Point1):
        return True if Point1.distance() <= self.r ** 2 else False


p1 = Point1(6, 7)
c1 = Circle1(9)
print(c1.belonging(p1))

p2 = Point1(3, 4)
c2 = Circle1(5)
print(c2.belonging(p2))



print('\nЦентр круга в ЛЮБОЙ точке:')

class Shape2:
    def __init__(self):
        pass


class Point2(Shape2):
    # xp, yp - координаты точки
    def __init__(self, xp, yp):
        self.xp = xp
        self.yp = yp


class Circle2(Shape2):
    # xc, yc - координаты центра окружности
    def __init__(self, xc, yc, r):
        self.xc = xc
        self.yc = yc
        self.r = r
    
    def belonging(self, Point2):
        between = (Point2.xp - self.xc) ** 2 + (Point2.yp - self.yc) ** 2 
        return True if between <= self.r ** 2 else False


p3 = Point2(3, 4)
c3 = Circle2(1, 2, 3)
print(c3.belonging(p3))

p4 = Point2(6, 7)
c4 = Circle2(3, 2, 5)
print(c4.belonging(p4))



# 1st task
class A:
    def __init__(self, num_elem):
        self.attr1 = list(range(num_elem))


class LazyObject:
    '''
    Class for deferred instantiation of objects.  Init is called
    only when the first attribute is either get or set.
    '''

    def __init__(self, callable, *args, **kw):
        '''
        callable -- Class of objeсt to be instantiated or functionnn to be called
        *args -- arguments to be used when instantiating object
        **kw  -- keywords to be used when instantiating object
        '''
        self.__dict__['callable'] = callable
        self.__dict__['args'] = args
        self.__dict__['kw'] = kw
        self.__dict__['obj'] = None

    def initObj(self):
        '''
        Instantiate object if not already done
        '''
        if self.obj is None:
            self.__dict__['obj'] = self.callable(*self.args, **self.kw)

    def __getattr__(self, name):
        self.initObj()
        return getattr(self.obj, name)

    def __setattr__(self, name, value):
        self.initObj()
        setattr(self.obj, name, value)

    def __len__(self):
        self.initObj()
        return len(self.obj)

    def __getitem__(self, idx):
        self.initObj()
        return self.obj[idx]
    
    @property
    def reset(self):
        return self.args
    
    @reset.setter
    def reset(self, value):
        if value == 1:
            self.obj is None
        else:
            pass


# a = LazyObject(A, num_elem=10**8)
# print(1 in a.attr1)
# print(42 in a.attr1)
# a.reset = 1
# print(42 in a.attr1)



import time


class Timer():
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = time.time()
        return None

    def __exit__(self, type, value, traceback):
        elapsed_time = (time.time() - self.start) * 1000
        print(self.message.format(elapsed_time))
