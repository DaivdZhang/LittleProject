import math


class Fraction(object):
    precision = 16

    def __init__(self, numerator, denominator=1):
        """

        :type numerator: int
        :type denominator: int
        """
        if not (isinstance(numerator, int) and isinstance(denominator, int)):
            raise ValueError("expected <class 'int'>")
        if denominator == 0:
            raise ZeroDivisionError

        x = math.gcd(numerator, denominator)
        self.numerator = numerator//x
        self.denominator = denominator//x
        if self.numerator < 0 and self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
        elif self.denominator < 0 < self.numerator:
            self.numerator = -self.numerator
            self.denominator = -self.denominator

    def __str__(self):
        if self.denominator == 1:
            return "Fraction(" + str(self.numerator) + ')'
        string = "Fraction(" + '/'.join([str(self.numerator), str(self.denominator)]) + ')'
        return string
    __repr__ = __str__

    def __bool__(self):
        if self == Fraction(0):
            return False
        else:
            return True

    def __eq__(self, other):
        """

        :type other: Fraction
        """
        if self.numerator == other.numerator and self.denominator == other.denominator:
            return True
        else:
            return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True

    def __lt__(self, other):
        if (self - other).numerator*(self - other).denominator < 0:
            return True
        else:
            return False

    def __le__(self, other):
        """

        :type other: Fraction
        """
        if (self - other).numerator*(self - other).denominator <= 0:
            return True
        else:
            return False

    def __gt__(self, other):
        """

        :type other: Fraction
        """
        if self < other:
            return False
        else:
            return True

    def __ge__(self, other):
        """

        :type other: Fraction
        """
        if self <= other:
            return False
        else:
            return True

    def __neg__(self):
        return Fraction(-1)*self

    def __abs__(self):
        a = abs(self.numerator)
        b = abs(self.denominator)
        return Fraction(a, b)

    def __add__(self, other):
        """

        :type other: Fraction
        """
        a = self.numerator*other.denominator + other.numerator*self.denominator
        b = self.denominator*other.denominator
        return Fraction(a, b)
    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other):
        """

        :type other: Fraction
        """
        return self + (-other)
    __rsub__ = __sub__
    __isub__ = __sub__

    def __mul__(self, other):
        """

        :type other: Fraction
        """
        a = self.numerator*other.numerator
        b = self.denominator*other.denominator
        return Fraction(a, b)
    __rmul__ = __mul__
    __imul__ = __mul__

    def __truediv__(self, other):
        """

        :type other: Fraction
        """
        a = other.numerator
        b = other.denominator
        return self*Fraction(b, a)
    __rdiv__ = __truediv__
    __idiv__ = __truediv__

    def __pow__(self, power, modulo=None):
        if not isinstance(power, int):
            raise ValueError("expected <class 'int'> got %s instead" % type(power))

        if power >= 0:
            return Fraction(self.numerator**power, self.denominator**power)
        else:
            return Fraction(self.denominator**(-power), self.numerator**(-power))
    __ipow__ = __pow__

    @staticmethod
    def set_precision(n):
        """

        :type n: int
        """
        Fraction.precision = n

    def tof(self):
        x = self.numerator
        y = self.denominator
        i, x = divmod(x, y)
        x *= 10**(Fraction.precision + len(str(y)) - 1)
        f, x = divmod(x, y)
        return str(i) + '.' + str(f)

    @classmethod
    def from_float(cls, num):
        """

        :type num: float
        """
        if not isinstance(num, float):
            if isinstance(num, int):
                return cls(num)
            else:
                raise ValueError("expected <class 'float'> got %s instead" % type(num))

        n = str(num)
        prec = len(n.split('.')[1])
        n = int(float(n)*10**prec)
        return cls(n, 10**prec)
