# my module
from graph.lowlink import *
# my module
class TwoEdgeConnectedComponents:
    def __init__(self, g) -> None:
        N = len(g)
        self.g = g
        self.low = LowLink(g)
        self.comp = comp = [-1] * N
        self.k = 0
        for i in range(N):
            if comp[i] == -1: self._dfs(i, -1)
        self.groups = groups = [[] for _ in range(self.k)]
        self.tree = tree = [[] for _ in range(self.k)]
        for i, x in enumerate(comp): groups[x].append(i)
        for uv in self.low.bridge:
            u, v = comp[uv >> 20], comp[uv & 0xfffff]
            tree[u].append(v)

    def __getitem__(self, k: int) -> int:
        return self.comp[k]

    def _dfs(self, i: int, p: int) -> None:
        q = [[i, p]]
        while q:
            i, p = q.pop()
            if p >= 0 and self.low.ord[p] >= self.low.low[i]:
                self.comp[i] = self.comp[p]
            else:
                self.comp[i] = self.k
                self.k += 1
            for d in self.g[i]:
                if self.comp[d] == -1:
                    q.append([d, i])

