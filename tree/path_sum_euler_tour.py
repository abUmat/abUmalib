# my module
from data_structure.bit import *
from data_structure.sparse_table import *
from tree.euler_tour import *
# my module

class PathSum:
    def __init__(self, G, A, root=0):
        N = len(G)
        ete, etv, self.in_, self.out, depth = euler_tour(root, G)
        arr1 = [depth[v]<<20|v for v in etv]
        self.st = SparseTable(arr1)
        arr2 = [0] * (N<<1)
        for i, e in enumerate(ete):
            arr2[i] += A[e]
            A[e] = -A[e]
        self.bit = BIT(N<<1, arr2)

    def lca(self, u, v):
        x, y = self.in_[u], self.in_[v]
        if x > y: x, y = y, x
        res = self.st.query(x, y+1)
        return res&0xfffff

    def add(self, p, x):
        self.bit.add(self.in_[p], x)
        self.bit.add(self.out[p], -x)

    def vertex_query(self, u, v):
        lca = self.lca(u, v)
        return self.bit.pref(self.in_[u]+1) + self.bit.pref(self.in_[v]+1) - (self.bit.pref(self.in_[lca]+1)<<1) + self.bit[self.in_[lca]]

    def edge_query(self, u, v):
        lca = self.lca(u, v)
        return self.bit.pref(self.in_[u]+1) + self.bit.pref(self.in_[v]+1) - (self.bit.pref(self.in_[lca]+1)<<1)

