import random
import time
from functools import reduce


class Matrix(object):
    def __init__(self, mat=None):
        if mat is None:
            self.matrix = []
        else:
            self.matrix = mat
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
            result += [_add(self.matrix[i], other.matrix[i])]
        return Matrix(result)

    def __mul__(self, other):
        def n_mul(mat, n):
            result = []
            for i in range(mat.get_shape()[0]):
                result.append([n * x for x in mat.matrix[i]])
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
                    temp += [_mul(mat1.matrix[i], mat2.matrix[j])]
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
        t_matrix = []
        if not self.matrix:
            return []
        for j in range(self.shape[1]):
            t_matrix.append([self.matrix[i][j] for i in range(self.shape[0])])
        return Matrix(t_matrix)

    def inv(self):  # TODO: finish the inv function
        pass

    @staticmethod
    def det(mat):
        if mat.shape[0] != mat.shape[1]:
            raise IndexError

        for j in range(mat.shape[0]):
            for i in range(j+1, mat.shape[0]):
                k = mat.matrix[i][j]/mat.matrix[j][j]
                mat.matrix[i] = list(map(lambda x, y: y - k*x, mat.matrix[j], mat.matrix[i]))
        main_diagonal = map(lambda x: mat.get(x, x), [row for row in range(mat.shape[0])])
        return reduce(lambda x, y: x*y, main_diagonal)

    def get_shape(self):
        if self.matrix:
            return len(self.matrix), len(self.matrix[0])
        else:
            return None

    def zero(self, row=3, col=3):
        for y in range(row):
            self.matrix += [[0*x for x in range(col)]]
        self.shape = (row, col)

    def eye(self, n=2):
        self.zero(row=n, col=n)
        for i in range(n):
            self.matrix[i][i] = 1
        self.shape = self.get_shape()

    def rand(self, row, col):
        random.seed(time.time())
        self.zero(row, col)
        for i in range(self.get_shape()[0]):
            self.matrix[i] = list(map(lambda x: x + random.random(), self.matrix[i]))
        self.shape = self.get_shape()

    def get(self, row, col):
        if row >= self.get_shape()[0] or col >= self.get_shape()[1]:
            raise IndexError
        return self.matrix[row][col]

    def mprint(self):
        for i in range(self.get_shape()[0]):
            if i == 0:
                print('[')
                print(self.matrix[i])
            elif i == self.get_shape()[0] - 1:
                print(self.matrix[i])
                print(']')
            else:
                print(self.matrix[i])
