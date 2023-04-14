# my module
from data_structure.bit import *
from tree.euler_tour import *
# my module

class SubtreeSum:
    def __init__(self, G, A, root=0):
        N = len(G)
        ete, _, self.in_, self.out, _ = euler_tour(root, G)
        arr = [0] * (N<<1)
        for i, e in enumerate(ete):
            arr[i] += A[e]
            A[e] = 0
        self.bit = BIT(N<<1, arr)

    def add(self, p, x):
        self.bit.add(self.in_[p], x)

    def query(self, u):
        return self.bit.sum(self.in_[u], self.out[u])
