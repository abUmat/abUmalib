# my module
from graph.lowlink import *
# my module
# https://nyaannyaan.github.io/library/graph/biconnected-components.hpp
class BiConnectedComponents(LowLink):
    def __init__(self, g: Graph) -> None:
        super().__init__(g)
        self.tmp: List[Pair]= []
        self.bc: List[List[int]]= []
        self.used: List[int]= [0] * self.n
        self._build()

    def _build(self) -> None:
        for i in range(len(self.used)):
            if not self.used[i]:
                self._dfs(i, -1)

    def _dfs(self, idx: int, par: int) -> None:
        self.used[idx] = 1
        for to in self.g[idx]:
            if to == par: continue
            if not self.used[to] or self.ord[to] < self.ord[idx]:
                if idx < to:
                    self.tmp.append((idx, to))
                else:
                    self.tmp.append((to, idx))
            if not self.used[to]:
                self._dfs(to, idx)
                if self.low[to] >= self.ord[idx]:
                    self.bc.append([])
                    while 1:
                        e = self.tmp.pop()
                        self.bc[-1].append(e)
                        if e[0] == min(idx, to) and e[1] == max(idx, to):
                            break