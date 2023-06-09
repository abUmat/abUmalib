# my module
from misc.typing_template import *
# my module
# # https://nyaannyaan.github.io/library/graph/strongly-connected-components.hpp
class StronglyConnectedComponents:
    def __init__(self, g: Graph) -> None:
        self._g = g
        self._used = [0] * len(g)
        self._order: List[int]= []
        self._build()

    def __getitem__(self, k: int) -> int:
        return self._comp[k]

    def belong(self, i: int) -> List[int]:
        return self._blng[i]

    def _dfs(self, s: int) -> None:
        q = [s]
        while q:
            v = q.pop()
            if v >= 0:
                if self._used[v]: continue
                q.append(~v)
                self._used[v] = 1
                for vv in self._g[v]:
                    q.append(vv)
            else:
                self._order.append(~v)

    def _rdfs(self, s: int, cnt: int) -> None:
        q = [s]
        while q:
            v = q.pop()
            if v >= 0:
                if self._comp[v] != -1: continue
                self._comp[v] = cnt
                for vv in self._rg[v]:
                    q.append(vv)

    def _build(self) -> None:
        for v in range(len(self._g)): self._dfs(v)
        self._order.reverse()
        self._comp = comp = [-1] * len(self._g)
        self._rg = rg = [[] for _ in range(len(self._g))]
        for v in range(len(self._g)):
            for vv in self._g[v]:
                rg[vv].append(v)
        ptr = 0
        for v in self._order:
            if comp[v] == -1:
                self._rdfs(v, ptr)
                ptr += 1
        self.dag: List[List[int]] = [[] for _ in range(ptr)]
        self._blng: List[List[int]] = [[] for _ in range(ptr)]
        for v in range(len(self._g)):
            self._blng[comp[v]].append(v)
            for vv in self._g[v]:
                x = comp[v]
                y = comp[vv]
                if x == y: continue
                self.dag[x].append(y)
