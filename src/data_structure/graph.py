from copy import deepcopy as _deepcopy


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
        return self._out_edges(vi, self.unconnected)

    def _out_edges(self, vi, unconnected):
        return [(i, value) for i, value in enumerate(self.matrix[vi]) if value != unconnected]

    def add_vertex(self, unconnected=self.unconnected):
        new_row = [unconnected]*self.vertex_num
        self.matrix.append(new_row)
        self.vertex_num = self._get_vnum()
        for row in self.matrix:
            row.append(unconnected)
