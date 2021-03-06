import random
import time
from functools import reduce
from copy import copy as _copy
from copy import deepcopy as _deepcopy
try:
    from simplejson import dumps, load
except ImportError:
    from json import dumps, load
import math
import re


def _from_string(string):
    if string[-1] == ';':
        string = string[: len(string) - 1]
    if ',' in string:
        string = string.replace(',', ' ')

    row_string = string.split(';')
    array = [row.split(' ') for row in row_string]

    def _not_empty(x):
        return x.strip() and x

    array = [filter(_not_empty, row) for row in array]
    array = [[float(x) for x in row] for row in array]
    return array


class Matrix(object):

    def __init__(self, data=None):
        if data is None:
            self.array = [[]]
        else:
            try:
                self.array = Matrix.from_string(data).array
            except AttributeError:
                self.array = [[element for element in row] for row in data]
                if len(set([len(row) for row in self.array])) != 1:
                    raise IndexError
        self.shape = self._get_shape()

    def __getitem__(self, item):
        """

        >>> m = Matrix([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        >>> m
        [[1.0 2.0]
         [3.0 4.0]
         [5.0 6.0]]
        >>> m[0: 2, :]
        [[1.0 2.0]
         [3.0 4.0]]
        >>> m[2, 1]
        6.0
        """
        ret = self.get(item)
        try:
            return Matrix(ret)
        except TypeError:
            return ret

    def __setitem__(self, key, value):
        """

        usage:
            >>> m = Matrix([[1.5, 2, 3], [4.1, 5, 6], [7.7, 8, 9]])
            >>> m
            [[1.5 2 3]
             [4.1 5 6]
             [7.7 8 9]]
            >>> m[0: 2, 0: 1] = [[8.1], [9.0]]
            >>> m
            [[8.1 2 3]
             [9.0 5 6]
             [7.7 8 9]]
            >>> m = Matrix([[1.5, 2, 3], [4.1, 5, 6], [7.7, 8, 9]])
            >>> m
            [[1.5 2 3]
             [4.1 5 6]
             [7.7 8 9]]
            >>> m[0, 0] = 8.1
            >>> m
            [[8.1 2 3]
             [4.1 5 6]
             [7.7 8 9]]
        """
        try:
            col_range = [key[1].start, key[1].stop]
            if key[1].start is None:
                col_range[0] = 0
            if key[1].stop is None:
                col_range[1] = self.shape[1]
            array = self.array[key[0]]

            for i, row in enumerate(array):
                del row[key[1]]
                for j in range(col_range[0], col_range[1]):
                    row.insert(j, value[i][j])
        except AttributeError:
            self.array[key[0]][key[1]] = value

    def __contains__(self, item):
        for row in self.array:
            if item in row:
                return True
        else:
            return False

    def __iter__(self):
        self.__i = 0
        self.__j = 0
        return self

    def __next__(self):
        """

        >>> m0 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> for i in m0:
        ...     print(i)
        ...
        1
        2
        3
        4
        5
        6
        7
        8
        9
        """
        if self.__i == self.shape[0]:
            raise StopIteration

        element = self.array[self.__i][self.__j]
        self.__j += 1
        if self.__j == self.shape[1]:
            self.__j = 0
            self.__i += 1

        return element

    def __str__(self):
        string = []
        if not Matrix.print_all:
            for i, row in enumerate(self.array):
                if self.shape[0] > 64 and 8 < i < self.shape[0] - 8:
                    continue
                elif self.shape[0] > 64 and i == self.shape[0] - 8:
                    string.append("......")
                else:
                    if self.shape[1] > 64:
                        a = ' '.join(map(str, row[0: 4]))
                        b = ' '.join(map(str, row[self.shape[1]-4:]))
                        string.append('[' + a + "......" + b + ']')
                    else:
                        string.append('[' + ' '.join(map(str, row))+']')
        else:
            for row in self.array:
                string.append('[' + ' '.join(map(str, row)) + ']')

        return '[' + "\n ".join(string) + "]\n"

    def __repr__(self):
        tmp = str(self)
        return tmp[: len(tmp)-1]

    def __bool__(self):
        if self.array != [[]]:
            return True
        else:
            return False

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

    def __gt__(self, other):
        result = []
        if self.shape == other.shape:
            for x, y in zip(self, other):
                if x > y:
                    result.append(1)
                else:
                    result.append(0)
        else:
            raise IndexError
        return Matrix.from_list(result, self.shape)

    def __lt__(self, other):
        _ = self >= other
        return Matrix.from_list(map(lambda x: not x, _.flat()), self.shape)

    def __ge__(self, other):
        result = []
        if self.shape == other.shape:
            for x, y in zip(self, other):
                if x >= y:
                    result.append(1)
                else:
                    result.append(0)
        else:
            raise IndexError
        return Matrix.from_list(result, self.shape)

    def __le__(self, other):
        _ = self > other
        return Matrix.from_list(map(lambda x: not x, _.flat()), self.shape)

    def __pos__(self):
        return self

    def __neg__(self):
        return -1*self

    def __abs__(self):
        array = [[abs(element) for element in row] for row in self.array]
        return Matrix(array)

    def __add__(self, other):
        if self.shape != other.shape:
            raise IndexError("two mats don't have the same shape.")
        try:
            result = []
            tmp = []
            for row1, row2 in zip(self.array, other.array):
                for element1, element2 in zip(row1, row2):
                    tmp.append(element1 + element2)
                result.append(tmp)
                tmp = []
            return Matrix(result)
        except AttributeError:
            return Matrix([[element + other for element in row] for row in self.array])
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

            def _mul(arr1, arr2):
                return sum([x*y for x, y in zip(arr1, arr2)])

            tmp = []
            mat2 = mat2.transpose
            for i in range(mat1.shape[0]):
                for j in range(mat2.shape[0]):
                    tmp.append(_mul(mat1.array[i], mat2.array[j]))
                result.append(tmp)
                tmp = []
            return result

        try:
            return Matrix(mat_mul(self, other))
        except AttributeError:
            return Matrix(num_mul(self, other))
    __imul__ = __mul__
    __rmul__ = __mul__

    def __sub__(self, other):
        return self + (-other)
    __isub__ = __sub__
    __rsub__ = __sub__

    def __truediv__(self, other):
        """

        :type other: int, float
        """
        try:
            return (1/other)*self
        except AttributeError:
            AttributeError("num type expected not {0}".format(type(other)))
    __itruediv__ = __truediv__

    def __floordiv__(self, other):
        """

        :type other: int, float
        """
        return Matrix([[element//other for element in row] for row in self.array])
    __ifloordiv__ = __floordiv__

    def __mod__(self, other):
        """

        :type other: int, float
        """
        return Matrix([[element % other for element in row] for row in self.array])
    __imod__ = __mod__

    def __floor__(self):
        return Matrix([[math.floor(element) for element in row] for row in self.array])

    def __ceil__(self):
        return Matrix([[math.ceil(element) for element in row] for row in self.array])

    def __pow__(self, power):
        if self.shape[0] != self.shape[1]:
            raise IndexError("square matrix expected")

        m = Matrix.eye(self.shape[0])
        try:
            for i in range(power):
                m *= self
            return m
        except TypeError:
            raise TypeError("<class 'int'> expected got {0}".format(type(power)))
    __ipow__ = __pow__

    def __copy__(self):
        cls = self.__class__
        new_mat = cls()
        new_mat.__dict__.update(self.__dict__)
        return new_mat

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}

        cls = self.__class__
        new_mat = cls()
        memodict[id(self)] = new_mat
        for key, item in self.__dict__.items():
            setattr(new_mat, key, _deepcopy(item, memodict))
        return new_mat

    def copy(self):
        return self.__copy__()

    def deepcopy(self):
        return self.__deepcopy__()

    @staticmethod
    def pw_product(mat1, mat2):
        """
        :type mat1: Matrix
        :type mat2: Matrix

        usage:
        >>> m0 = Matrix([[1, 2, 3.1], [4, 5, 6], [7, 8, 9]])
        >>> m0
        [[1 2 3.1]
         [4 5 6]
         [7 8 9]]
        >>> m1 = Matrix([[1.5, 2.3, 3], [4.1, 5, 6], [7.7, 8, 9]])
        >>> m1
        [[1.5 2.3 3]
         [4.1 5 6]
         [7.7 8 9]]
        >>> Matrix.pw_product(m0, m1)
        [[1.5 4.6 9.3]
         [16.4 25 36]
         [53.9 64 81]]
        """
        if mat1.shape != mat2.shape:
            raise IndexError("two mats don't have the same shape")

        result = []
        for row1, row2 in zip(mat1.array, mat2.array):
            tmp = [element1*element2 for element1, element2 in zip(row1, row2)]
            result.append(tmp)
        return Matrix(result)

    @property
    def transpose(self):
        """

        :rtype: Matrix

        get transpose of the matrix
        """
        if not self.array:
            return None
        t_array = [[row[j] for row in self.array] for j in range(self.shape[1])]
        return Matrix(t_array)

    @staticmethod
    def _transform(array, row, identity=False):
        """

        :rtype: list, int

        Transfer the matrix to a lower triangular matrix or a diagonal matrix according to the
        arg identity.
        """
        count = 0
        for j in range(row):
            for i in range(j+1, row):
                if not array[j][j]:
                    _ = [x for x in range(i, row) if array[x][j]]
                    if _:
                        _ = _.pop(0)
                    else:
                        return array, count
                    array[j], array[_] = array[_], array[j]
                    count += 1
                k = array[i][j]/array[j][j]
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
        """

        To solve the inverse matrix of the given matrix.
        """
        if mat.shape[0] != mat.shape[1]:
            raise IndexError("square matrix expected")
        if Matrix.det(mat) == 0:
            return None
        if not mat:
            return mat

        array = _deepcopy(mat.array)
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
    def __solve_i(self):
        return Matrix.inv(self)

    @staticmethod
    def det(mat):
        """

        Solve the determinant of the square matrix.
        """
        array = _copy(mat.array)
        # avoid changing the elements in the matrix.
        # The reason of using copy instead of deepcopy is due to the function _transform.

        if mat.shape[0] != mat.shape[1]:
            raise IndexError
        if mat.shape[0] == mat.shape[1] == 0:
            return 1

        array, count = Matrix._transform(array, mat.shape[0])
        main_diagonal = [array[i][i] for i in range(mat.shape[0])]
        return reduce(lambda x, y: x*y, main_diagonal)*(-1)**count

    @property
    def trace(self):
        if self.shape[0] != self.shape[1]:
            raise IndexError("square matrix expected")
        return sum([row[i] for i, row in enumerate(self.array)])

    @property
    def rank(self):
        """

        Get the rank of the square matrix.
        """
        # TODO: check if there still exist bugs.

        if self.shape[0] != self.shape[1]:
            raise IndexError("square matrix expected")

        array = Matrix._transform(self.array, self.shape[0])[0]
        count = 0
        for row in array:
            if len(set(row)) > 1:
                count += 1
        return count

    def _get_shape(self):
        if self:
            return len(self.array), len(self.array[0])
        else:
            return 0, 0

    def reshape(self, shape):
        """

        :type shape: tuple

        >>> m0 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> m0.reshape((1, 9))
        >>> m0
        [[1 2 3 4 5 6 7 8 9]]
        >>> m0.reshape((9, 1))
        >>> m0
        [[1]
         [2]
         [3]
         [4]
         [5]
         [6]
         [7]
         [8]
         [9]]
         >>> m0.reshape((3, 3))
         >>> m0
         [[1 2 3]
          [4 5 6]
          [7 8 9]]
        """
        if self.shape[0]*self.shape[1] != shape[0]*shape[1]:
            raise IndexError

        new_array = []
        tmp = []
        for i, element in enumerate(self):
            tmp.append(element)
            if (i+1) % shape[1] == 0:
                new_array.append(tmp)
                tmp = []
        self.array = new_array
        self.shape = self._get_shape()
        # return self if unittest needed

    def fill(self, value):
        """

        Filling the matrix with the specific value.
        This will change the matrix itself.

        >>> m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> m
        [[1 2 3]
         [4 5 6]
         [7 8 9]]
        >>> m.fill(-1)
        >>> m
        [[-1 -1 -1]
         [-1 -1 -1]
         [-1 -1 -1]]
        """
        for ind, element in enumerate(self):
            i, j = divmod(ind, self.shape[1])
            self.array[i][j] = value

    def flat(self):
        """

        Turn the matrix to a list and return a generator.
        """
        return (x for x in self)

    def repeat(self, repeats, axis):
        """

        Generate a matrix by repeating each row of the given matrix.

        >>> m = Matrix([[1, 2], [4, 5], [7, 8]])
        >>> m.repeat(2, 0)
        [[1 2]
         [1 2]
         [4 5]
         [4 5]
         [7 8]
         [7 8]]
        >>> m.repeat(2, 1)
        [[1 2 1 2]
         [4 5 4 5]
         [7 8 7 8]]
        >>> m.repeat([1, 2, 3], 0)
        [[1 2]
         [4 5]
         [4 5]
         [7 8]
         [7 8]
         [7 8]]
        """
        if isinstance(repeats, int):
            repeats = [repeats]*self.shape[0]

        new_arr = []
        if axis == 0:
            array = [[row]*i for row, i in zip(self.array, (x for x in repeats))]
            for row in array:
                new_arr.extend(row)
        else:
            for ind, i in enumerate(repeats):
                new_arr.append(self.array[ind]*i)
        mat = Matrix(new_arr)
        del new_arr

        return mat

    def tile(self, reps):
        """

        :type reps: tuple, list

        Generate a matrix by repeating the given matrix.

        >>> m = Matrix([[1, 2, 3], [2, 4, 6], [7, 8, 9]])
        >>> m.tile((2, 1))
        [[1 2 3]
         [2 4 6]
         [7 8 9]
         [1 2 3]
         [2 4 6]
         [7 8 9]]
        >>> m.tile((1, 2))
        [[1 2 3 1 2 3]
         [2 4 6 2 4 6]
         [7 8 9 7 8 9]]
        >>> m.tile((1, 0))
        [[]]
        >>> m.tile((0, 2))
        [[1 2 3 1 2 3]
         [2 4 6 2 4 6]
         [7 8 9 7 8 9]]
        >>> m.tile((0, 1))
        [[1 2 3]
         [2 4 6]
         [7 8 9]]
        """
        array = _deepcopy(self.array)
        for i in range(reps[0]-1):
            array += array
        mat = Matrix(array)
        if reps[1] == 0:
            return Matrix()
        mat = mat.repeat(reps[1], 1)
        return mat

    @classmethod
    def zero(cls, row=3, col=3):
        """

        Generate a matrix filled with 0.
        """
        array = [[0]*col]*row
        return cls(array)

    @classmethod
    def eye(cls, n):
        """

        Generate a identity matrix.
        """
        mat = cls.zero(row=n, col=n)
        for i in range(n):
            mat.array[i][i] = 1
        return mat

    @classmethod
    def rand(cls, row, col):
        """

        Generate a matrix filled with random number whose range is from 0 to 1.
        """
        random.seed(time.time())
        mat = cls.zero(row, col)
        for i in range(row):
            mat.array[i] = [element + random.random() for element in mat.array[i]]
        return mat

    def index(self, x, total=False):
        col = self.shape[1]
        indexes = [divmod(i, col) for i, element in enumerate(self) if element == x]
        if total:
            return indexes
        else:
            return indexes[0]

    def get(self, index):
        """

        :type index: tuple
        """
        return self.array[index[0]][index[1]]

    def max(self, axis=None):
        """
        :type axis: int

        Get maximum of the matrix.
        The value of the axis decides how to calculate.

        >>> m0 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> m0.max()
        9
        >>> m0.max(0)
        [[3]
         [6]
         [9]]
        >>> m0.max(1)
        [[7 8 9]]
        """
        if axis == 0:
            return Matrix([[max(row) for row in self.array]]).T
        elif axis == 1:
            return Matrix([[max(row) for row in self.transpose.array]])
        elif axis is None:
            return max(self)

    def min(self, axis=None):
        """

        :type axis: int

        Get minimum of the matrix.
        The value of the axis decides how to calculate.

        >>> m0 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> m0.min()
        1
        >>> m0.min(0)
        [[1]
         [4]
         [7]]
        >>> m0.min(1)
        [[1 2 3]]
        """
        if axis == 0:
            return Matrix([[min(row) for row in self.array]]).T
        elif axis == 1:
            return Matrix([[min(row) for row in self.transpose.array]])
        elif axis is None:
            return min(self)

    def mean(self, axis=None):
        """

        :type axis: int

        Calculate the average of the elements of the matrix.
        The value of the axis decides how to calculate.

        >>> m0 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> m0.mean()
        5.0
        >>> m0.mean(0)
        [[2.0]
         [5.0]
         [8.0]]
        >>> m0.mean(1)
        [[4.0 5.0 6.0]]
        """
        element_num = self.shape[0]*self.shape[1]
        if axis == 0:
            return Matrix([[sum(row)/self.shape[1] for row in self.array]]).T
        elif axis == 1:
            return Matrix([[sum(row)/self.shape[0] for row in self.transpose.array]])
        elif axis is None:
            return sum([sum(row) for row in self.array])/element_num

    def var(self, axis=None):
        """

        :type axis: int

        Solve the variance of the matrix.
        The value of the axis decides how to calculate.

        >>> m0 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> m0.var()
        6.666666666666667
        >>> m0.var(0)
        [[0.6666666666666666]
         [0.6666666666666666]
         [0.6666666666666666]]
        >>> m0.var(1)
        [[6.0 6.0 6.0]]
        """
        if axis == 0:
            return Matrix([[Matrix([row]).var() for row in self.array]]).T
        elif axis == 1:
            return self.transpose.var(0).T
        elif axis is None:
            average = self.mean()
            return Matrix([[(x - average)**2 for x in self]]).mean()

    def std(self, axis=None):
        """

        :type axis: int

        m0.std() is equal to m0.var()**0.5
        The value of the axis decides how to calculate.
        """
        if axis is None:
            return self.var(axis)**0.5
        elif axis == 0:
            return Matrix([[x**0.5 for x in self.var(axis)]]).T
        elif axis == 1:
            return Matrix([[x**0.5 for x in self.var(axis)]])

    def sum(self, axis=None):
        """

        >>> m = Matrix([[1.0, 0, -3], [2, -5, 4], [1, -3, 9]])
        >>> m
        [[1.0 0 -3]
         [2 -5 4]
         [1 -3 9]]
        >>> m.sum()
        6.0
        >>> m.sum(0)
        [[-2.0]
         [1]
         [7]]
        >>> m.sum(1)
        [[4.0 -8 10]]
        """
        if axis == 0:
            return Matrix([[sum(row) for row in self.array]]).T
        elif axis == 1:
            return Matrix([[sum(row) for row in self.transpose.array]])
        elif axis is None:
            return sum([sum(row) for row in self.array])

    def sort(self, axis=None, key=None, reverse=False):
        """

        This function can sort the elements of the matrix, which will change the matrix itself.

        >>> m = Matrix([[1.0, 0, -3], [2, -5, 4], [1, -3, 9]])
        >>> m.sort()
        >>> m
        [[-5 -3 -3]
         [0 1.0 1]
         [2 4 9]]
        >>> m.sort(axis=0)
        >>> m
        [[-5 -3 -3]
         [0 1.0 1]
         [2 4 9]]
        >>> m.sort(axis=1)
        >>> m
        [[-5 -3 -3]
         [0 1.0 1]
         [2 4 9]]
        >>> m.sort(axis=0, key=abs)
        >>> m
        [[-3 -3 -5]
         [0 1.0 1]
         [2 4 9]]
        >>> m.sort(axis=0, key=abs, reverse=True)
        >>> m
        [[-5 -3 -3]
         [1.0 1 0]
         [9 4 2]]
        >>> m.sort(axis=0, key=lambda x: x**3)
        >>> m
        [[-5 -3 -3]
         [0 1.0 1]
         [2 4 9]]
        """
        if axis is None:
            shape = self.shape
            self.reshape((1, self.shape[0]*self.shape[1]))
            self.array[0].sort(key=key, reverse=reverse)
            self.reshape(shape)
        elif axis == 0:
            for row in self.array:
                row.sort(key=key, reverse=reverse)
        elif axis == 1:
            mat = self.transpose
            for row in mat.array:
                row.sort(key=key, reverse=reverse)
            self.array = mat.transpose.array

    @classmethod
    def from_string(cls, string):
        """
        :type string: str

        Generate the matrix from a string.

        >>> m = Matrix.from_string("1 2;3 4;5 6")
        >>> m
        [[1.0 2.0]
         [3.0 4.0]
         [5.0 6.0]]
        """
        array = _from_string(string)
        return Matrix(array)

    @classmethod
    def from_list(cls, array, shape):
        """

        :type array: iterable
        :type shape: tuple, list

        Generate a matrix from a one-dimensional array.
        List, tuple or generator is accepted.

        >>> m = Matrix.from_list([x for x in range(6)], (3, 2))
        >>> m
        [[0 1]
         [2 3]
         [4 5]]
        >>> m = Matrix.from_list((x for x in range(6)), (3, 2))
        >>> m
        [[0 1]
         [2 3]
         [4 5]]
        """
        mat = cls([array])
        mat.reshape(shape)
        return mat

    @classmethod
    def from_file(cls, filename):
        i = filename.index('.')
        if filename[i+1:] == "json":
            return cls.mload(filename)
        elif filename[i+1:] == "txt":
            with open(filename, 'r', encoding="UTF-8") as file:
                strings = file.readlines()
                string = ''.join(map(str.strip, strings))
            return cls.from_string(string)

    def to_string(self):
        """

        Transfer the matrix to a string.

        >>> m = Matrix.from_string("1 2;3 4;5 6")
        >>> m .to_string()
        '1.0 2.0;3.0 4.0;5.0 6.0'
        """
        string = []
        for row in self.array:
            string.append(' '.join(map(str, row)))
        return ';'.join(string)

    def to_list(self):
        return self.array

    def to_file(self, filename: str, mode='J'):
        if '.' in filename:
            i = filename.index('.')
            if mode == 'J':
                filename = filename[: i] + ".json"
            elif mode == 'T':
                filename = filename[: i] + ".txt"

        if mode == 'J':
            self.mdump(filename)
        elif mode == 'T':
            string = self.to_string()
            strings = string.split(';')
            string = ";\n".join(strings) + '\n'
            with open(filename, 'w', encoding="UTF-8") as file:
                file.write(string)

    def mdump(self, filename):
        """

        Dump the matrix into a json file.
        """
        pattern = re.compile("..*\.json")
        if not re.match(pattern, filename):
            raise ValueError("invalid filename. json file expected.")

        json = dumps(self.array, indent='')
        with open(filename, 'w', encoding="UTF-8") as file:
            file.write(json)

    @classmethod
    def mload(cls, filename):
        """

        Load the data in a json file, and turn the data into the matrix.
        """
        with open(filename, 'r', encoding="UTF-8") as file:
            return cls(load(fp=file))

    # The following is class attributes
    I = __solve_i
    T = transpose
    print_all = False  # decide whether displaying the full matrix.
