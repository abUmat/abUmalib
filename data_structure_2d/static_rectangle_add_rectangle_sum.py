# my module
from data_structure.bit import *
# my module
# https://judge.yosupo.jp/submission/100406
from bisect import bisect_left
from collections import deque
mod = 18446744069414584321
class Weight:
    def __init__(self, a: int=0, b: int=0) -> None:
        self.a, self.b = a, b
    def __add__(self, other):
        return Weight(self.a + other.a, self.b + other.b)
    def __sub__(self, other):
        return Weight(self.a - other.a, self.b - other.b)
    def __mul__(self, r: int):
        return Weight((self.a * r) % mod, (self.b * r) % mod)

class A:
    def __init__(self, a: Weight=None, b: Weight=None) -> None:
        if a is None: a = Weight()
        if b is None: b = Weight()
        self.a: Weight = a
        self.b: Weight = b
    def __add__(self, other):
        return A(self.a + other.a, self.b + other.b)
    def __sub__(self, other):
        return A(self.a - other.a, self.b - other.b)

class StaticRectangleAddRectangleSum:
    class Query:
        def __init__(self, l: int, d: int, r: int, u: int) -> None:
            self.l, self.d, self.r, self.u = l, d, r, u
    class WeightedRectangle:
        def __init__(self, l: int, d: int, r: int, u: int, w: int) -> None:
            self.l, self.d, self.r, self.u, self.w = l, d, r, u, w
    class InitQuery:
        def __init__(self, y: int, l: int, r: int, w: int) -> None:
            self.y, self.l, self.r, self.w = y, l, r, w

    def __init__(self, n: int, q: int) -> None:
        self.points_x: List[int] = [0] * (n << 1)
        self.rectangles: List[StaticRectangleAddRectangleSum.WeightedRectangle] = [0] * n
        self.queries: List[StaticRectangleAddRectangleSum.Query] = [0] * q
        self.pid = 0
        self.qid = 0

    def add_rectangle(self, l: int, d: int, r: int, u: int, w: int) -> None:
        self.points_x[self.pid << 1 | 0] = l
        self.points_x[self.pid << 1 | 1] = r
        self.rectangles[self.pid] = self.WeightedRectangle(l, d, r, u, w)
        self.pid += 1

    def add_query(self, l: int, d: int, r: int, u: int) -> None:
        self.queries[self.qid] = self.Query(l, d, r, u)
        self.qid += 1

    def build(self) -> None:
        InitQuery = self.InitQuery
        compress = {a: i for i, a in enumerate(sorted(set(self.points_x)))}
        init_queries: List[InitQuery] = [0] * (self.pid << 1)
        for i, rectangle in enumerate(self.rectangles):
            l, r = compress[rectangle.l], compress[rectangle.r]
            init_queries[i << 1 | 0] = InitQuery(rectangle.d, l, r, rectangle.w)
            init_queries[i << 1 | 1] = InitQuery(rectangle.u, l, r, -rectangle.w)
        self.init_queries: deque[InitQuery] = deque(sorted(init_queries, key=lambda q: q.y))
        self.compressed = list(compress.keys())

    def solve(self) -> None:
        def bit_pref(x: int) -> Weight:
            p = bisect_left(self.compressed, x)
            res = A()
            while p:
                res += bit[p - 1]
                p ^= p & -p
            return res.b + res.a * x

        def bit_sum(l: int, r: int) -> Weight:
            return bit_pref(r) - bit_pref(l)

        def bit_add(p: int, val: Weight) -> None:
            x = A(val, val * (-self.compressed[p]))
            p += 1
            while p <= len(bit):
                bit[p - 1] += x
                p += p & -p

        class HQ:
            def __init__(self, y: int, i: int, way: int) -> None:
                self.y, self.i, self.way = y, i, way

        self.build()
        bit = [A() for _ in range(self.pid << 1)]
        hq: List[HQ] = [0] * (self.qid << 1)
        for i, query in enumerate(self.queries):
            hq[i << 1 | 0] = HQ(query.d, i, 0)
            hq[i << 1 | 1] = HQ(query.u, i, 1)
        hq.sort(key=lambda q: q.y)
        res = [0] * self.qid
        popleft, appendleft = self.init_queries.popleft, self.init_queries.appendleft
        for q in hq:
            while self.init_queries:
                ptr = popleft()
                if not ptr.y < q.y:
                    appendleft(ptr)
                    break
                w = ptr.w
                wy = w * ptr.y % mod
                bit_add(ptr.l, Weight(w, -wy))
                bit_add(ptr.r, Weight(-w, wy))
            i = q.i
            v = bit_sum(self.queries[i].l, self.queries[i].r)
            tmp = (v.a * q.y + v.b) % mod
            if q.way: res[i] += tmp
            else: res[i] -= tmp
        return [x % mod for x in res]
