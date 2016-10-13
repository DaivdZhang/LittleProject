from copy import deepcopy as _deepcopy


# TODO: add other features
# TODO: debug

__all__ = ["Decimal"]


def _from_string(string):
    n = string
    if '-' in string:
        n = n.replace('-', '')
        neg = True
    else:
        neg = False

    if '.' in string:
        i, d = n.split('.')
        if d[-1] == '0':
            tmp = [x for x in d]
            for ind, _ in enumerate(tmp[::-1]):
                if _ == '0' and ind != len(tmp) - 1:
                    tmp.pop()
                else:
                    break
            d = "".join(tmp)
    else:
        i, d = n, '0'
    if i == d == '0':
        neg = False
    return neg, i, d


def _add(a, b):
    """

    :type a: Decimal
    :type b: Decimal
    """
    _ = abs(a.digits - b.digits)
    y = int(a.int_part) + int(b.int_part)
    if a.digits > b.digits:
        b.dec_part += '0'*_
    else:
        a.dec_part += '0'*_
    a.dec_part = '1' + a.dec_part
    b.dec_part = '1' + b.dec_part
    x = str(int(a.dec_part) + int(b.dec_part))
    if x[0] == '2':
        x = x[1:]
    else:
        x = x[1:]
        y += 1
    return Decimal(str(y) + '.' + x)


def _sub(a, b):
    """

    :type a: Decimal
    :type b: Decimal
    """
    _ = abs(a.digits - b.digits)
    if a.digits > b.digits:
        b.dec_part += '0'*_
        _ = a.digits
    else:
        a.dec_part += '0'*_
        _ = b.digits
    x = int(a.int_part + a.dec_part)
    y = int(b.int_part + b.dec_part)
    ret = str(x - y)
    neg = True if '-' in ret else False
    if neg:
        ret = ret.replace('-', '')
    ret = '0'*_ + ret
    ret = '-' + ret if neg else ret
    return Decimal(ret[: len(ret)-_] + '.' + ret[len(ret)-_:])


class Decimal(object):
    def __init__(self, num=None):
        try:
            self.neg, self.int_part, self.dec_part = _from_string(num)
        except TypeError:
            self.neg, self.int_part, self.dec_part = False, '0', '0'

        self.digits = len(self.dec_part)

    def __str__(self):
        if not self.neg:
            return "Decimal(" + self.int_part + '.' + self.dec_part + ')'
        else:
            return "Decimal(-" + self.int_part + '.' + self.dec_part + ')'
    __repr__ = __str__

    def __int__(self):
        return int(self.int_part)

    def __eq__(self, other):
        if self.int_part == other.int_part and self.dec_part == other.dec_part:
            if self.neg == other.neg:
                return True
            else:
                return False
        else:
            return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True

    def __lt__(self, other):
        result = self - other
        return result.neg

    def __le__(self, other):
        if self < other or self == other:
            return True
        else:
            return False

    def __gt__(self, other):
        if self <= other:
            return False
        else:
            return True

    def __ge__(self, other):
        if self < other:
            return False
        else:
            return True

    def __pos__(self):
        return self

    def __neg__(self):
        num = self.__copy__()
        num.neg = not num.neg
        return num

    def __add__(self, other):
        if self.neg and other.neg:
            return -_add(self, other)
        elif other.neg:
            return _sub(self, other)
        elif self.neg:
            return _sub(other, self)
        else:
            return _add(self, other)
    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other):
        if self.neg and other.neg:
            return _sub(other, self)
        elif other.neg:
            return self + (-other)
        elif self.neg:
            return -(-self + other)
        else:
            return _sub(self, other)
    __rsub__ = __sub__
    __isub__ = __sub__

    def __mul__(self, other):
        x = (int(self.int_part)*10**self.digits+int(self.dec_part))
        y = (int(other.int_part)*10**other.digits+int(other.dec_part))
        x = str(x*y)[:: -1]
        x, y = x[self.digits + other.digits:], x[0: self.digits + other.digits]
        x, y = x[::-1], y[::-1]
        if x == '':
            x = '0'
        if self.neg != other.neg:
            x = '-' + x
        return Decimal(x + '.' + y)
    __rmul__ = __mul__
    __imul__ = __mul__

    def __truediv__(self, other):
        x = int(self.int_part + self.dec_part)
        y = int(other.int_part + other.dec_part)
        _ = abs(self.digits - other.digits)
        if self.digits > other.digits:
            y *= 10**_
        elif self.digits < other.digits:
            x *= 10**_
        i, x = divmod(x, y)
        x *= 10**(len(str(y)) - len(str(x)))
        f, x = divmod(x, y)
        if self.neg != other.neg:
            i = '-' + str(i)
        return Decimal(str(i) + '.' + str(f))
    __rtruediv__ = __truediv__
    __itruediv__ = __truediv__

    def __floordiv__(self, other):
        return int(self/other)
    __rfloordiv__ = __floordiv__
    __ifloordiv__ = __floordiv__

    def __copy__(self):
        cls = self.__class__
        new_dec = cls()
        new_dec.__dict__.update(self.__dict__)
        return new_dec

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}

        cls = self.__class__
        new_dec = cls()
        memodict[id(self)] = new_dec
        for key, item in self.__dict__.items():
            setattr(new_dec, key, _deepcopy(item, memodict))
        return new_dec
