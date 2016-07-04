import random
import time
from functools import reduce


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
        def n_mul(mat, n):
            result = []
            for i in range(mat.get_shape()[0]):
                result.append([n * x for x in mat.array[i]])
            return result

        def m_mul(mat1, mat2):
            result = []
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

    def inv(self):  # TODO: finish the inv function
        if self.shape[0] != self.shape[1]:
            raise IndexError

    def det(self):
        if self.shape[0] != self.shape[1]:
            raise IndexError

        for j in range(self.shape[0]):
            for i in range(j+1, self.shape[0]):
                k = self.array[i][j]/self.array[j][j]
                self.array[i] = list(map(lambda x, y: y - k*x, self.array[j], self.array[i]))
        main_diagonal = map(lambda x: self.get(x, x), [row for row in range(self.shape[0])])
        return reduce(lambda x, y: x*y, main_diagonal)

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

    def get(self, row, col):
        if row >= self.shape[0] or col >= self.shape[1]:
            raise IndexError
        return self.array[row][col]

    def mprint(self):
        for i in range(self.shape[0]):
            if i == 0:
                print('[')
                print(self.array[i])
            elif i == self.shape[0] - 1:
                print(self.array[i])
                print(']')
            else:
                print(self.array[i])
