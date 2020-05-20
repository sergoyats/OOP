# 1st task: the decorator @once guarantees a single function call
def once(f):
    result = {}
    def inner(*args, **kwargs):
        if f not in result:
            result[f] = f(*args, **kwargs)
        return result[f]
    return inner


@once
def get_logger():
    return [1, 2, 3] * 2


l = get_logger()
l2 = get_logger()
print(id(l))
print(id(l2))
print('')


# 2nd task (see line 140 at once)
import re


class Descriptor:
    def __init__(self, name=None, default=None):
        self.name = name
        self.default = default

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance, objtype):
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self.default
        return instance.__dict__[self.name]

    def __delete__(self, instance):
        raise AttributeError("Can't delete")


class Typed(Descriptor):
    type_ = object
    extra_methods = []

    def __set__(self, instance, value):
        if not isinstance(value, self.type_):
            raise TypeError('Expected %s' % self.type_)
        super().__set__(instance, value)


# Specialized types
class Numeric(Typed):
    extra_methods = ['gt', 'gte']

    def gt(instance_value, value):
        return instance_value > value

    def gte(instance_value, value):
        return instance_value >= value


class Integer(Numeric):
    type_ = int


class Float(Numeric):
    type_ = float
    extra_methods = Numeric.extra_methods + ['isclose']

    def isclose(instance_value, value):
        import math
        return math.isclose(instance_value, value)


class String(Typed):
    type_ = str
    extra_methods = ['startswith', 'endswith', 'contains']

    def startswith(instance_value, value):
        return instance_value.startswith(value)

    def endswith(instance_value, value):
        return instance_value.endswith(value)

    def contains(instance_value, value):
        return value in instance_value


# Value checking
class Positive(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super().__set__(instance, value)


# More specialized types
class PosInteger(Integer, Positive):
    pass


class PosFloat(Float, Positive):
    pass


# Length checking
class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super().__set__(instance, value)


class SizedString(String, Sized):
    pass


# Pattern matching
class Regex(Descriptor):
    def __init__(self, *args, pattern, **kwargs):
        self.pattern = re.compile(pattern)
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pattern.match(value):
            raise ValueError('Invalid string')
        super().__set__(instance, value)


class SizedRegexString(SizedString, Regex):
    pass


class Range(Descriptor):
    def __init__(self, name, min_value, max_value):
        super().__init__(name)
        self.min_value, self.max_value = min_value, max_value

    def __set__(self, instance, value):
        if value < self.min_value or value > self.max_value:
            raise ValueError('The value is not in the required range')
        super().__set__(instance, value)


class RangeInteger(Integer, Range):
    pass


class ModelMeta(type):
    def __new__(metacls, clsname, bases=None, clsdict=None):
        cls = super().__new__(metacls, clsname, bases, clsdict)
        extra_attrs = []
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, Typed):
                extra_attrs += [
                    (attr_name, extra_method, getattr(attr_value.__class__, extra_method))
                    for extra_method in attr_value.extra_methods
                ]
        for attr, extra, func in extra_attrs:
            setattr(
                cls,
                f'{attr}__{extra}',
                lambda self, value, attr=attr, func=func: func(getattr(self, attr), value)
            )
        return cls


class Employee:
    first_name = SizedString(name='first_name', default='John', maxlen=32)
    last_name = SizedString(name='last_name', maxlen=64)
    age = PosInteger(name='age', default=42)
    salary = PosFloat(name='salary')
    phone_number = SizedRegexString(name='phone_number', maxlen=11, pattern='\d{3}-\d{7}')
    kpi_score = RangeInteger(name='kpi_score', min_value=0, max_value=100)


emp = Employee()
emp.kpi_score = 10
emp.kpi_score = 101 # exception
