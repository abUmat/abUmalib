# my module
from misc.typing_template import *
# my module
# https://github.com/not522/ac-library-python/blob/master/atcoder/mincostflow.py
from heapq import heappush, heappop
class MCFGraph:
    class _Edge:
        def __init__(self, dst: int, cap: int, cost: int) -> None:
            self.dst = dst
            self.cap = cap
            self.cost = cost
            self.rev: Optional[MCFGraph._Edge] = None

    def __init__(self, n: int) -> None:
        self._n = n
        self._g: List[List[MCFGraph._Edge]] = [[] for _ in range(n)]
        self._edges: List[MCFGraph._Edge] = []

    def add_edge(self, src: int, dst: int, cap: int, cost: int) -> int:
        m = len(self._edges)
        e = MCFGraph._Edge(dst, cap, cost)
        re = MCFGraph._Edge(src, 0, -cost)
        e.rev = re
        re.rev = e
        self._g[src].append(e)
        self._g[dst].append(re)
        self._edges.append(e)
        return m

    def get_edge(self, i: int) -> List[int]:
        assert 0 <= i < len(self._edges)
        e = self._edges[i]
        re = e.rev
        return [re.dst, e.dst, e.cap + re.cap, re.cap, e.cost]

    def edges(self) -> List[List[int]]:
        '''return: src, dst, cap, flow, cost'''
        return [self.get_edge(i) for i in range(len(self._edges))]

    def flow(self, s: int, t: int,
             flow_limit: Optional[int] = None) -> Pair:
        return self.slope(s, t, flow_limit)[-1]

    def slope(self, s: int, t: int,
              flow_limit: Optional[int] = None) -> List[Pair]:
        if flow_limit is None:
            flow_limit = sum(e.cap for e in self._g[s])

        dual = [0] * self._n
        prev: List[Optional[Tuple[int, MCFGraph._Edge]]] = [None] * self._n

        def refine_dual() -> bool:
            pq = [s]
            visited = bytearray(self._n)
            dist: List[Optional[int]] = [(1 << 60) - 1] * self._n
            dist[s] = 0
            while pq:
                tmp = heappop(pq)
                dist_v, v = tmp >> 30, tmp & 0x3fffffff
                if visited[v]: continue
                visited[v] = 1
                if v == t: break
                dual_v = dual[v]
                for e in self._g[v]:
                    w = e.dst
                    if visited[w] or e.cap == 0: continue
                    reduced_cost = e.cost - dual[w] + dual_v
                    new_dist = dist_v + reduced_cost
                    dist_w = dist[w]
                    if new_dist < dist_w:
                        dist[w] = new_dist
                        prev[w] = v, e
                        heappush(pq, (new_dist << 30 | w))
            else:
                return 0
            dist_t = dist[t]
            for v, dist_v in enumerate(dist):
                if visited[v]: dual[v] -= dist_t - dist[v]
            return 1

        flow = 0
        cost = 0
        prev_cost_per_flow: Optional[int] = None
        result = [(flow, cost)]
        while flow < flow_limit:
            if not refine_dual(): break
            f = flow_limit - flow
            v = t
            while prev[v] is not None:
                u, e = prev[v]
                f = min(f, e.cap)
                v = u
            v = t
            while prev[v] is not None:
                u, e = prev[v]
                e.cap -= f
                # assert e.rev is not None
                e.rev.cap += f
                v = u
            c = -dual[s]
            flow += f
            cost += f * c
            if c == prev_cost_per_flow: result.pop()
            result.append((flow, cost))
            prev_cost_per_flow = c
        return result
