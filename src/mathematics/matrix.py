import random
import time
from functools import reduce
from copy import copy, deepcopy
try:
    from simplejson import dumps, load
except ImportError:
    from json import dumps, load
from decimal import Decimal, getcontext

getcontext().prec = 16


class Matrix(object):
    def __init__(self, array=None):
        if array is None:
            self.array = [[]]
        else:
            self.array = [[Decimal(str(element)) for element in row] for row in array]  # improve the accuracy
        self.shape = self._get_shape()

    def __getitem__(self, item):
        return Matrix([[element for element in row[item[1]]] for row in self.array[item[0]]])

    def __setitem__(self, key, value):
        """

        usage:
            >>>> m = Matrix([[1.5, 2, 3], [4.1, 5, 6], [7.7, 8, 9]])
            >>>> m
            [[1.5 2 3]
             [4.1 5 6]
             [7.7 8 9]]
            >>>> m[0: 2, 0: 1] = [[8.1], [9.0]]
            >>>> m
            [[8.1 2 3]
             [9.0 5 6]
             [7.7 8 9]]
            or
            >>>> m = Matrix([[1.5, 2, 3], [4.1, 5, 6], [7.7, 8, 9]])
            >>>> m
            [[1.5 2 3]
             [4.1 5 6]
             [7.7 8 9]]
            >>>> m[0, 0] = 8.1
            >>>> m
            [[8.1 2 3]
             [4.1 5 6]
             [7.7 8 9]]
        """
        if isinstance(key[0], int):
            self.array[key[0]][key[1]] = Decimal(str(value))
        else:
            col_range = [key[1].start, key[1].stop]
            if key[1].start is None:
                col_range[0] = 0
            if key[1].stop is None:
                col_range[1] = self.shape[1]
            array = self.array[key[0]]

            for i, row in enumerate(array):
                del row[key[1]]
                for j in range(col_range[0], col_range[1]):
                    row.insert(j, Decimal(str(value[i][j])))

    def __str__(self):
        string = []
        for row in self.array:
            string.append('['+' '.join(map(lambda x: str(x), row))+']')
        return '[' + '\n '.join(string) + ']'
    __repr__ = __str__

    def __eq__(self, other):
        for row1, row2 in zip(self.array, other.array):
            if row1 != row2:
                return False
        else:
            return True

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True

    def __neg__(self):
        return -1*self

    def __add__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        result = []
        if self.shape != other.shape:
            raise IndexError

        tmp = []
        for row1, row2 in zip(self.array, other.array):
            for element1, element2 in zip(row1, row2):
                tmp.append(element1 + element2)
            result.append(tmp)
            tmp = []
        return Matrix(result)
    __iadd__ = __add__
    __radd__ = __add__

    def __mul__(self, other):
        result = []

        def num_mul(mat, n):
            for i in range(mat.shape[0]):
                result.append([n*x for x in mat.array[i]])
            return result

        def mat_mul(mat1, mat2):
            if mat1.shape[1] != mat2.shape[0]:
                raise IndexError

            def _mul(list1, list2):
                tmp = 0
                for element1, element2 in zip(list1, list2):
                    tmp += element1*element2
                return tmp

            temp = []
            mat2 = mat2.transpose
            for i in range(mat1.shape[0]):
                for j in range(mat2.shape[0]):
                    temp.append(_mul(mat1.array[i], mat2.array[j]))
                result.append(temp)
                temp = []
            else:
                return result

        if isinstance(other, int) or isinstance(other, float):
            return Matrix(num_mul(self, other))
        else:
            return Matrix(mat_mul(self, other))
    __imul__ = __mul__
    __rmul__ = __mul__

    def __sub__(self, other):
        return self + (-other)
    __isub__ = __sub__
    __rsub__ = __sub__

    def __pow__(self, power):
        if not isinstance(power, int):
            raise ValueError
        if self.shape[0] != self.shape[1]:
            raise IndexError

        m = Matrix.eye(self.shape[0])
        while power:
            m = m*self
            power -= 1
        return m
    __ipow__ = __pow__

    @staticmethod
    def pw_product(mat1, mat2):
        """
        :type mat1: Matrix
        :type mat2: Matrix

        usage:
        >>>> m0 = Matrix([[1, 2, 3.2], [4, 5, 6], [7, 8, 9]])
        >>>> m0
        [[1 2 3.2]
         [4 5 6]
         [7 8 9]]
        >>>> m1 = Matrix([[1.5, 2.3, 3], [4.1, 5, 6], [7.7, 8, 9]])
        >>>> m1
        [[1.5 2.3 3]
         [4.1 5 6]
         [7.7 8 9]]

        >>>> Matrix.pw_product(m0, m1)
        [[1.5 4.6 9.6]
         [16.4 25 36]
         [53.9 64 81]]
        """
        if mat1.shape != mat2.shape:
            raise IndexError

        result = []
        tmp = []
        for row1, row2 in zip(mat1.array, mat2.array):
            for element1, element2 in zip(row1, row2):
                tmp.append(element1*element2)
            result.append(tmp)
            tmp = []
        return Matrix(result)

    @property
    def transpose(self):
        if not self.array:
            return None
        t_array = [[row[j] for row in self.array] for j in range(self.shape[1])]
        return Matrix(t_array)

    @staticmethod
    def _transform(array, row, identity=False):
        count = 0
        for j in range(row):
            for i in range(j+1, row):
                if not array[j][j]:
                    _ = [x for x in range(i, row) if array[x][j]].pop(0)
                    array[j], array[_] = array[_], array[j]
                    count += 1
                try:
                    k = array[i][j]/array[j][j]
                except ZeroDivisionError:
                    if not sum(array[j]):
                        return 0, count
                array[i] = list(map(lambda x, y: y - k*x, array[j], array[i]))

        if identity:
            for j in range(row-1, -1, -1):
                for i in range(j-1, -1, -1):
                    if not array[j][j]:
                        array[j], array[i] = array[i], array[j]
                    k = array[i][j]/array[j][j]
                    array[i] = list(map(lambda x, y: y - k*x, array[j], array[i]))
        return array, count

    @staticmethod
    def inv(mat):
        if mat.shape[0] != mat.shape[1]:
            raise IndexError
        if Matrix.det(mat) == 0:
            return None

        array = deepcopy(mat.array)
        e = Matrix.eye(mat.shape[0])
        for i, row in enumerate(array):
            row.extend(e.array[i])

        array = Matrix._transform(array, mat.shape[0], True)[0]
        for i in range(mat.shape[0]):
            if array[i][i] != 1:
                array[i] = list(map(lambda x: x/array[i][i], array[i]))

        for row in array:
            del row[0: mat.shape[0]]
        return Matrix(array)

    @property
    def solve_i(self):
        return Matrix.inv(self)

    @staticmethod
    def det(mat):
        array = copy(mat.array)
        if mat.shape[0] != mat.shape[1]:
            raise IndexError

        array, count = Matrix._transform(array, mat.shape[0])
        main_diagonal = [array[i][i] for i in range(mat.shape[0])]
        return reduce(lambda x, y: x*y, main_diagonal)*(-1)**count

    @staticmethod
    def trace(mat):
        return reduce(lambda x, y: x+y, [mat.array[i][i] for i in range(mat.shape[0])])

    def _get_shape(self):
        if self.array:
            return len(self.array), len(self.array[0])
        else:
            return None

    @classmethod
    def zero(cls, row=3, col=3):
        array = []
        for y in range(row):
            array.append([0]*col)
        return cls(array)

    @classmethod
    def eye(cls, n=2):
        mat = cls.zero(row=n, col=n)
        for i in range(n):
            mat.array[i][i] = 1
        return mat

    @classmethod
    def rand(cls, row, col):
        random.seed(time.time())
        mat = cls.zero(row, col)
        for i in range(row):
            mat.array[i] = [element + random.random() for element in mat.array[i]]
        return mat

    def index(self, x, total=False):
        indexes = []
        for i, row in enumerate(self.array):
            for j, element in enumerate(row):
                if element == x:
                    indexes.append((i, j))
        if total:
            return indexes
        else:
            return indexes[0]

    @staticmethod
    def mdump(mat, filename="matrix.json"):
        json = dumps(mat.array, indent='')
        with open(filename, 'w', encoding="UTF-8") as file:
            file.write(json)

    @staticmethod
    def mload(filename):
        with open(filename, 'r', encoding="UTF-8") as file:
            return Matrix(load(fp=file))

    # The following is class attributes
    I = solve_i
    T = transpose
