# my module
from misc.typing_template import *
# my module
# https://nyaannyaan.github.io/library/tree/centroid-decomposition.hpp
class CentroidDecomposition:
    def __init__(self, g: Graph, isbuild: bool=1) -> None:
        self.g = g
        self.sub = [0] * len(g)
        self.v = bytearray(len(g))
        if isbuild: self.build()

    def build(self) -> None:
        self.tree = [[] for _ in range(len(self.g))]
        self.root = self.build_dfs(0)

    def get_size(self, _cur: int) -> int:
        mask = (1 << 20) - 1
        q = [_cur << 20 | _cur]
        end = ~_cur << 20 | _cur
        while q:
            tmp = q.pop()
            cur, par = tmp >> 20, tmp & mask
            if cur >= 0:
                q.append(~cur << 20 | par)
                self.sub[cur] = 1
                for dst in self.g[cur]:
                    if dst == par or self.v[dst]: continue
                    q.append(dst << 20 | cur)
            else:
                if tmp == end: return self.sub[~cur]
                self.sub[par] += self.sub[~cur]

    def get_centroid(self, _cur: int, mid: int) -> int:
        mask = (1 << 20) - 1
        q = [_cur << 20 | _cur]
        end = ~_cur << 20 | _cur
        ans = -1
        while q:
            tmp = q.pop()
            cur, par = tmp >> 20, tmp & mask
            if cur >= 0:
                q.append(~cur << 20 | par)
                for dst in self.g[cur]:
                    if dst == par or self.v[dst]: continue
                    if self.sub[dst] > mid:
                        q.append(dst << 20 | cur)
                        break
            else:
                if ans == -1: ans = ~cur
                if tmp == end: return ans

    def build_dfs(self, cur: int) -> int:
        centroid = self.get_centroid(cur, self.get_size(cur) >> 1)
        self.v[centroid] = 1
        for dst in self.g[centroid]:
            if not self.v[dst]:
                nxt = self.build_dfs(dst)
                if centroid != nxt: self.tree[centroid].append(nxt)
        self.v[centroid] = 0
        return centroid
