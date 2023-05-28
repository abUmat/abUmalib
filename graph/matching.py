# my module
from graph.mf_graph import *
# my module
class Matching(MFGraph):
    def __init__(self, n: int, m: int) -> None:
        super().__init__(n + m + 2)
        self.L = n
        self.R = m
        self.s = n + m
        self.t = n + m + 1
        for i in range(n): super().add_edge(n + m, i, 1)
        for i in range(m): super().add_edge(i + n, n + m + 1, 1)

    def add_edge(self, n: int, m: int, cap: int=1) -> int:
        return super().add_edge(n, m + self.L, cap)

    def flow(self) -> int:
        return super().flow(self.s, self.t)

    def edges(self):
        es = super().edges()
        ret = []
        for e in es:
            if e.flow > 0 and e.frm != self.s and e.to != self.t:
                ret.append((e.frm, e.to - self.L))
        return ret