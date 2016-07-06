import random
import time
from functools import reduce
from copy import copy, deepcopy


class Matrix(object):
    def __init__(self, array=None):
        if array is None:
            self.array = []
        else:
            self.array = array
        self.shape = self.get_shape()

    def __add__(self, other):
        result = []
        if self.get_shape() != other.get_shape():
            raise IndexError

        def _add(list1, list2):
            list3 = []
            for j in range(len(list1)):
                list3 += [list1[j] + list2[j]]
            return list3

        for i in range(self.shape[0]):
            result += [_add(self.array[i], other.array[i])]
        return Matrix(result)

    def __mul__(self, other):
        result = []

        def n_mul(mat, n):
            for i in range(mat.get_shape()[0]):
                result.append([n*x for x in mat.array[i]])
            return result

        def m_mul(mat1, mat2):
            if mat1.shape[1] != mat2.shape[0]:
                raise IndexError

            def _mul(list1, list2):
                tmp = 0
                for _ in range(len(list1)):
                    tmp += list1[_] * list2[_]
                return tmp

            temp = []
            mat2 = mat2.t()
            for i in range(mat1.shape[0]):
                for j in range(mat1.shape[1]):
                    temp += [_mul(mat1.array[i], mat2.array[j])]
                result.append(temp)
                temp = []
            else:
                return result

        if isinstance(other, int) or isinstance(other, float):
            return Matrix(n_mul(self, other))
        else:
            return Matrix(m_mul(self, other))

    def __sub__(self, other):
        other *= -1
        return self + other

    def t(self):  # TODO: speed up transpose function
        if not self.array:
            return []
        t_array = [[row[j] for row in self.array] for j in range(self.shape[1])]
        return Matrix(t_array)

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

        for j in range(mat.shape[0]):
            for i in range(j+1, mat.shape[0]):
                if not array[j][j]:
                    array[j], array[i] = array[i], array[j]
                k = array[i][j]/array[j][j]
                array[i] = list(map(lambda x, y: y - k*x, array[j], array[i]))
        for j in range(mat.shape[0]-1, -1, -1):
            for i in range(j-1, -1, -1):
                if not array[j][j]:
                    array[j], array[i] = array[i], array[j]
                k = array[i][j]/array[j][j]
                array[i] = list(map(lambda x, y: y - k*x, array[j], array[i]))
        for i in range(mat.shape[0]):
            if array[i][i] != 1:
                array[i] = list(map(lambda x: x/array[i][i], array[i]))

        for row in array:
            del row[0: mat.shape[0]]
        return Matrix(array)

    @staticmethod
    def det(mat):
        array = copy(mat.array)
        if mat.shape[0] != mat.shape[1]:
            raise IndexError

        count = 0
        for j in range(mat.shape[0]-1):
            for i in range(j+1, mat.shape[0]):
                if not array[j][j]:
                    count += 1
                    array[j], array[i] = array[i], array[j]
                try:
                    k = array[i][j]/array[j][j]
                except ZeroDivisionError:
                    if not sum(array[j]):
                        return 0
                array[i] = list(map(lambda x, y: y - k*x, array[j], array[i]))
        main_diagonal = [array[i][i] for i in range(mat.shape[0])]
        return reduce(lambda x, y: x*y, main_diagonal)*(-1)**count

    @staticmethod
    def trace(mat):
        return reduce(lambda x, y: x+y, [mat.array[i][i] for i in range(mat.shape[0])])

    def get_shape(self):
        if self.array:
            return len(self.array), len(self.array[0])
        else:
            return None

    @classmethod
    def zero(cls, row=3, col=3):
        array = []
        for y in range(row):
            array += [[0 for x in range(col)]]
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
            mat.array[i] = list(map(lambda x: x + random.random(), mat.array[i]))
        return mat

    def get(self, row=-1, col=-1):
        if row >= self.shape[0] or col >= self.shape[1]:
            raise IndexError
        return self.array[row][col]

    def mprint(self):
        for i in range(self.shape[0]):
            if i == 0:
                print('[', end='')
                print(self.array[i])
            elif i == self.shape[0] - 1:
                print(self.array[i], end='')
                print(']')
            else:
                print(self.array[i])
