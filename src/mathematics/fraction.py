import math


class Fraction(object):
    precision = 16

    def __init__(self, numerator, denominator=1):
        """

        :type numerator: int, float
        :type denominator: int
        """
        if isinstance(numerator, float) and denominator == 1:
            self.numerator = Fraction.from_float(numerator).numerator
            self.denominator = Fraction.from_float(numerator).denominator
        elif isinstance(numerator, int) and isinstance(denominator, int):
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
        else:
            raise ValueError("expected <class 'int'>")

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

    def __pos__(self):
        return self

    def __neg__(self):
        return Fraction(-1)*self

    def __abs__(self):
        a = abs(self.numerator)
        b = abs(self.denominator)
        return Fraction(a, b)

    def __add__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)

        a = self.numerator*other.denominator + other.numerator*self.denominator
        b = self.denominator*other.denominator
        return Fraction(a, b)
    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return self + (-other)

    def __rsub__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return -self + other
    __isub__ = __sub__

    def __mul__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)

        a = self.numerator*other.numerator
        b = self.denominator*other.denominator
        return Fraction(a, b)
    __rmul__ = __mul__
    __imul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)

        a = other.numerator
        b = other.denominator
        return self*Fraction(b, a)

    def __rtruediv__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)

        return other*Fraction(self.denominator, self.numerator)
    __itruediv__ = __truediv__

    def __floordiv__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return int(self/other)

    def __rfloordiv__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return int(other/self)
    __ifloordiv__ = __floordiv__

    def __mod__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return Fraction.from_float(float(self - self//other*other))

    def __rmod__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return Fraction.from_float(float(other - other//self*self))
    __imod__ = __mod__

    def __floor__(self):
        return int(self)

    def __ceil__(self):
        return int(self) + 1

    def __pow__(self, power, modulo=None):
        if not isinstance(power, int):
            raise ValueError("expected <class 'int'> got %s instead" % type(power))

        if power >= 0:
            return Fraction(self.numerator**power, self.denominator**power)
        else:
            return Fraction(self.denominator**(-power), self.numerator**(-power))
    __ipow__ = __pow__

    def __int__(self):
        return int(self._to_float())

    def __float__(self):
        return self._to_float()

    def __copy__(self):
        cls = type(self)
        return cls(self.numerator, self.denominator)

    def copy(self):
        return self.__copy__()

    @staticmethod
    def set_precision(n):
        """

        :type n: int
        """
        Fraction.precision = n

    def _to_float(self):
        x = abs(self.numerator)
        y = self.denominator
        i, x = divmod(x, y)
        x *= 10**(Fraction.precision + len(str(y)) - 1)
        f, x = divmod(x, y)
        if self.numerator >= 0:
            return float(str(i) + '.' + str(f))
        else:
            return float('-' + str(i) + '.' + str(f))

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
