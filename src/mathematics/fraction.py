import math


class Fraction(object):
    precision = 16

    def __init__(self, nume, deno=1):
        if not (isinstance(nume, int) and isinstance(deno, int)):
            raise ValueError
        if deno == 0:
            raise ZeroDivisionError

        x = math.gcd(nume, deno)
        self.nume = nume//x
        self.deno = deno//x
        if self.nume < 0 and self.deno < 0:
            self.nume = abs(self.nume)
            self.deno = abs(self.deno)

    def __str__(self):
        if self.deno == 1:
            return "Fraction(" + str(self.nume) + ')'
        string = "Fraction(" + '/'.join([str(self.nume), str(self.deno)]) + ')'
        return string
    __repr__ = __str__

    def __bool__(self):
        if self == Fraction(0):
            return False
        else:
            return True

    def __eq__(self, other):
        if self.nume*self.deno == other.nume*other.deno:
            return True
        else:
            return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True

    def __lt__(self, other):
        if (self - other).nume*(self - other).deno < 0:
            return True
        else:
            return False

    def __le__(self, other):
        if (self - other).nume*(self - other).deno <= 0:
            return True
        else:
            return False

    def __gt__(self, other):
        if self < other:
            return False
        else:
            return True

    def __ge__(self, other):
        if self <= other:
            return False
        else:
            return True

    def __neg__(self):
        return Fraction(-1)*self

    def __abs__(self):
        a = abs(self.nume)
        b = abs(self.deno)
        return Fraction(a, b)

    def __add__(self, other):
        a = self.nume*other.deno + other.nume*self.deno
        b = self.deno*other.deno
        return Fraction(a, b)
    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other):
        return self + (-other)
    __rsub__ = __sub__
    __isub__ = __sub__

    def __mul__(self, other):
        a = self.nume*other.nume
        b = self.deno*other.deno
        return Fraction(a, b)
    __rmul__ = __mul__
    __imul__ = __mul__

    def __truediv__(self, other):
        a = other.nume
        b = other.deno
        return self*Fraction(b, a)
    __rdiv__ = __truediv__
    __idiv__ = __truediv__

    def __pow__(self, power, modulo=None):
        if not isinstance(power, int):
            raise ValueError

        if power >= 0:
            return Fraction(self.nume**power, self.deno**power)
        else:
            return Fraction(self.deno**(-power), self.nume**(-power))
    __ipow__ = __pow__

    @staticmethod
    def set_accuracy(n):
        Fraction.precision = n

    def tof(self):
        x = self.nume
        y = self.deno
        i, x = divmod(x, y)
        x *= 10**(Fraction.precision + len(str(y)) - 1)
        f, x = divmod(x, y)
        return str(i) + '.' + str(f)
