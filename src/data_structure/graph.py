from copy import deepcopy as _deepcopy


class GraphError(Exception):
    pass


class Graph(object):
    def __init__(self, matrix, unconnected=0):
        self.vertex_num = len(matrix)
        _ = {len(row) for row in matrix}
        if len(_) != 1 or self.vertex_num not in _:
            raise IndexError
        self.matrix = _deepcopy(matrix)
        self.unconnected = unconnected

    def __str__(self):
        strings = [' '.join(map(str, row))for row in self.matrix]
        return '\n'.join(strings) + "\nunconnected: {0}".format(self.unconnected)
    __repr__ = __str__

    def _get_vnum(self):
        return len(self.matrix)

    def add_edge(self, vi, vj, value=1):
        self.matrix[vi][vj] = value

    def get_edge(self, vi, vj):
        return self.matrix[vi][vj]

    def out_edges(self, vi):
        return self._out_edges(self.matrix, vi, self.unconnected)

    @staticmethod
    def _out_edges(matrix, vi, unconnected):
        return [(i, value) for i, value in enumerate(matrix[vi]) if value != unconnected]

    def add_vertex(self, unconnected=0):
        new_row = [unconnected]*self.vertex_num
        self.matrix.append(new_row)
        self.vertex_num = self._get_vnum()
        for row in self.matrix:
            row.append(unconnected)


class GraphAL(Graph):
    def __init__(self, matrix, unconnected=0):
        super().__init__(matrix, unconnected)
        self.matrix = [Graph.out_edges(self, i) for i in range(self.vertex_num)]

    def add_vertex(self, unconnected=0):
        self.matrix.append([])
        self.vertex_num = self._get_vnum()
        return self.vertex_num - 1

    def add_edge(self, vi, vj, value=1):
        if self.vertex_num == 0:
            raise GraphError("cannot add edge to a empty graph")

        i = 0
        row = self.matrix[vi]
        for i, _ in enumerate(row):
            if row[i][0] == vj:
                self.matrix[vi][i] = (vj, value)
                return None
            if row[i][0] > vj:
                break
        self.matrix[vi].insert(i+1, (vj, value))

    def get_edge(self, vi, vj):
        for i, value in self.matrix[vi]:
            if i == vj:
                return value
        else:
            return self.unconnected

    def out_edges(self, vi):
        return self.matrix[vi]
