# my module
from data_structure.rollback_unionfind import *
from misc.typing_template import *
from misc.antirec import *
# my module
# https://nyaannyaan.github.io/library/graph/offline-dynamic-connectivity.hpp
class OffLineDynamicConnectivity:
    def __init__(self, n: int, q: int) -> None:
        self.N = n
        self.Q = q
        self.uf = RollbackUnionFind(n)
        self.qadd: List[List[int]]= [[] for _ in range(q)]
        self.qdel: List[List[int]]= [[] for _ in range(q)]
        segsz = 1
        while segsz < q: segsz <<= 1
        self.segsz = segsz
        self.seg = [[] for _ in range(segsz << 1)]
        self.cnt = {}

    def add_edge(self, time: int, u: int, v: int) -> None:
        '''register add u-v edge at time'''
        if u > v: u, v = v, u
        self.qadd[time].append(u << 20 | v)

    def del_edge(self, time: int, u: int, v: int) -> None:
        '''register delete u-v edge at time'''
        if u > v: u, v = v, u
        self.qdel[time].append(u << 20 | v)

    def build(self) -> None:
        for i in range(self.Q):
            for e in self.qadd[i]:
                dat = self.cnt.get(e, 0)
                if not dat & 0xfffff:
                    self.cnt[e] = i << 20 | 1
                else:
                    self.cnt[e] += 1
            for e in self.qdel[i]:
                self.cnt[e] -= 1
                dat = self.cnt[e]
                if not dat & 0xfffff:
                    self._segment(e, dat >> 20, i)
        for e, dat in self.cnt.items():
            if dat & 0xfffff:
                self._segment(e, dat >> 20, self.Q)

    @antirec
    def _dfs(self, add, delete, query, id: int, l: int, r: int) -> None:
        if self.Q <= l: yield
        state = self.uf.get_state()
        es = []
        for x in self.seg[id]:
            u, v = x >> 20, x & 0xfffff
            if not self.uf.same(u, v):
                self.uf.union(u, v)
                add(u, v)
                es.append(x)
        if l + 1 == r:
            query(l)
        else:
            yield self._dfs(add, delete, query, id << 1 | 0, l, l + r >> 1)
            yield self._dfs(add, delete, query, id << 1 | 1, l + r >> 1, r)
        for x in es:
            delete(x >> 20, x & 0xfffff)
        self.uf.rollback(state)
        yield

    def run(self, add: Func20, delete: Func20, query: Func10) -> None:
        self._dfs(add, delete, query, 1, 0, self.segsz)

    def _segment(self, e: int, l: int, r: int) -> None:
        L = l + self.segsz
        R = r + self.segsz
        while L < R:
            if L & 1:
                self.seg[L].append(e)
                L += 1
            if R & 1:
                R ^= 1
                self.seg[R].append(e)
            L >>= 1
            R >>= 1

