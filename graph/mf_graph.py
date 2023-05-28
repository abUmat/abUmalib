from typing import List
from collections import deque
class MFGraph:
    class edge:
        def __init__(self, frm: int, to: int, cap: int, flow: int) -> None:
            self.frm = frm
            self.to = to
            self.cap = cap
            self.flow = flow

    class _edge:
        def __init__(self, to: int, rev: int, cap: int) -> None:
            self.to = to
            self.rev = rev
            self.cap = cap

    def __init__(self, n: int=0) -> None:
        self._n = n
        self.g = [[] for _ in range(n)]
        self.pos = []

    def add_edge(self, frm: int, to: int, cap: int) -> int:
        self.pos.append((frm, len(self.g[frm])))
        self.g[frm].append(self._edge(to, len(self.g[to]), cap))
        self.g[to].append(self._edge(frm, len(self.g[frm]) - 1, 0))
        return len(self.pos)

    def get_edge(self, i: int) -> edge:
        _e = self.g[self.pos[i][0]][self.pos[i][1]]
        _re = self.g[_e.to][_e.rev]
        return self.edge(self.pos[i][0], _e.to, _e.cap + _re.cap, _re.cap)

    def edges(self) -> List[edge]:
        return [self.get_edge(i) for i in range(len(self.pos))]

    def change_edge(self, i: int, new_cap: int, new_flow: int) -> None:
        _e = self.g[self.pos[i][0]][self.pos[i][1]]
        _re = self.g[_e.to][_e.rev]
        _e.cap = new_cap - new_flow
        _re.cap = new_flow

    def flow(self, s: int, t: int, flow_limit: int=0xfffffffffffffff) -> int:
        def bfs() -> List[int]:
            level = [-1] * self._n
            level[s] = 0
            que = deque()
            que.append(s)
            while que:
                v = que.popleft()
                for e in self.g[v]:
                    if e.cap == 0 or level[e.to] >= 0: continue
                    level[e.to] = level[v] + 1
                    if e.to == t: return
                    que.append(e.to)
            return level

        def dfs(v: int, up: int) -> int:
            if v == s: return up
            res = 0
            level_v = level[v]
            for i in range(iter[v], len(self.g[v])):
                e = self.g[v][i]
                if level_v <= level[e.to] or self.g[e.to][e.rev].cap == 0: continue
                d = dfs(e.to, min(up - res, self.g[e.to][e.rev].cap))
                if d <= 0: continue
                self.g[v][i].cap += d
                self.g[e.to][e.rev].cap -= d
                res += d
                if res == up: break
            return res

        flow = 0
        while flow < flow_limit:
            level = bfs()
            if level[t] == -1: break
            iter = [0] * len(self.g)
            while flow < flow_limit:
                f = dfs(t, flow_limit - flow)
                if not f: break
                flow += f
        return flow

    def min_cut(self, s: int) -> bytearray:
        visited = bytearray(self._n)
        q = deque()
        q.append(s)
        while q:
            p = q.popleft()
            visited[p] = 1
            for e in self.g[p]:
                if e.cap and not visited[e.to]:
                    visited[e.to] = 1
                    q.append(e.to)
        return visited
