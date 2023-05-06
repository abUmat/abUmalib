# my module
from tree.euler_tour import *
from data_structure.sparse_table import *
# my module
class LCA:
    def __init__(self, root, G):
        _, etv, self.in_, _, depth = euler_tour(root, G)
        arr = [depth[v]<<20|v for v in etv]
        self.st = SparseTable(arr)
    def query(self, u, v):
        x, y = self.in_[u], self.in_[v]
        if x > y: x, y = y, x
        res = self.st.query(x, y+1)
        return res&0xfffff
