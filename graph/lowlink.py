# my module
from misc.typing_template import *
# my module
# https://nyaannyaan.github.io/library/graph/lowlink.hpp
class LowLink:
    def __init__(self, g: Graph) -> None:
        self.g = g
        self.n = n = len(g)
        self.ord = ord = [-1] * n
        self.low = [-1] * n
        self.bridge: List[int]= []
        self.articulation: List[int]= []
        k = 0
        for i, x in enumerate(ord):
            if x == -1:
                k = self.dfs(i, k, -1)

    def dfs(self, idx: int, k: int, par: int) -> int:
        ord, low = self.ord, self.low
        k += 1
        low[idx] = ord[idx] = k
        cnt = 0
        arti = 0; second = 0
        for to in self.g[idx]:
            if ord[to] == -1:
                cnt += 1
                k = self.dfs(to, k, idx)
                low[idx] = min(low[idx], low[to])
                arti |= (par != -1) & (low[to] >= ord[idx])
                if ord[idx] < low[to]:
                    if idx < to: self.bridge.append(idx << 20 | to)
                    else: self.bridge.append(to << 20 | idx)
            elif to != par or second:
                low[idx] = min(low[idx], ord[to])
            else:
                second = 1
        arti |= (par == -1) & (cnt > 1)
        if arti: self.articulation.append(idx)
        return k
