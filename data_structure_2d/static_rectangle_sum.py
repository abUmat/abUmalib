# my module
from data_structure.bit import *
# my module
# https://ei1333.github.io/library/other/static-point-add-rectangle-sum.hpp
class StaticRectangleSum:
    class _Point:
        def __init__(self, x: int, y: int, w: int) -> None:
            self.x, self.y, self.w = x, y, w

    class _Query:
        def __init__(self, l: int, d: int, r: int, u: int) -> None:
            self.l, self.d, self.r, self.u = l, d, r, u

    def __init__(self, n: int=0, q: int=0) -> None:
        self._points: List[StaticRectangleSum._Point] = [0] * n
        self._queries: List[StaticRectangleSum._Query] = [0] * q
        self._pid = 0
        self._qid = 0

    def add_point(self, x: int, y: int, w: int) -> None:
        self._points[self._pid] = self._Point(x, y, w)
        self._pid += 1

    def add_query(self, l: int, d: int, r: int, u: int) -> None:
        self._queries[self._qid] = self._Query(l, d, r, u)
        self._qid += 1

    def solve(self) -> List[int]:
        from bisect import bisect_left
        class Q:
            def __init__(self, x: int, d: int, u: int, type_: bool, idx: int) -> None:
                self.x, self.d, self.u, self.type, self.idx = x, d, u, type_, idx

        n, q = self._pid, self._qid
        points, queries = self._points, self._queries
        points.sort(key=lambda p: p.y)
        ys: List[int] = []
        for p in points:
            if not ys or ys[-1] != p.y: ys.append(p.y)
            p.y = len(ys) - 1
        qs: List[Q] = [0] * (q << 1)
        for i, query in enumerate(queries):
            d = bisect_left(ys, query.d)
            u = bisect_left(ys, query.u)
            qs[i << 1 | 0] = Q(query.l, d, u, 0, i)
            qs[i << 1 | 1] = Q(query.r, d, u, 1, i)

        points.sort(key=lambda p: p.x)
        qs.sort(key=lambda q: q.x)
        res = [0] * q
        j = 0
        bit = BIT(len(ys))
        for query in qs:
            while j < n and points[j].x < query.x:
                bit.add(points[j].y, points[j].w)
                j += 1
            if query.type: res[query.idx] += bit.sum(query.d, query.u)
            else: res[query.idx] -= bit.sum(query.d, query.u)
        return res
