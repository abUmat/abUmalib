from collections import deque
# my module
from misc.typing_template import *
# my module
class MFGraph:
    def __init__(self, n: int) -> None:
        self.n = n
        self.g: List[List[List[int]]] = [[] for _ in range(n)]
        self.pos = []

    def add_edge(self, src: int, dst: int, cap: int) -> int:
        self.pos.append((src, len(self.g[src])))
        self.g[src].append([dst, cap, len(self.g[dst])])
        self.g[dst].append([src, 0, len(self.g[src]) - 1])
        return len(self.pos)

    def get_edge(self, i: int) -> List[int]:
        src, eidx = self.pos[i]
        e_dst, e_cap, e_revidx = self.g[src][eidx]
        re_dst, re_cap, re_revidx = self.g[e_dst][e_revidx]
        return [src, e_dst, e_cap + re_cap, re_cap]

    def edges(self) -> List[List[int]]:
        return [self.get_edge(i) for i in range(len(self.pos))]

    def change_edge(self, i: int, new_cap: int, new_flow: int) -> None:
        src, eidx = self.pos[i]
        e = self.g[src][eidx]
        re = self.g[e[0]][e[2]]
        e[1] = new_cap - new_flow
        re[1] = new_flow

    def flow(self, s: int, t: int, flow_limit: Optional[int] = None) -> int:
        if flow_limit is None:
            flow_limit = sum(e[1] for e in self.g[s])

        def bfs() -> List[int]:
            level = [-1] * self.n
            level[s] = 0
            que = deque()
            que.append(s)
            while que:
                v = que.popleft()
                for to, cap, revidx in self.g[v]:
                    if (not cap) or level[to] >= 0: continue
                    level[to] = level[v] + 1
                    if to == t: return level
                    que.append(to)
            return level

        def dfs(lim: int) -> int:
            stack = []
            edge_stack: List[List[int]] = []
            stack.append(t)
            while stack:
                v = stack.pop()
                if v == s:
                    flow = min(lim, min(e[1] for e in edge_stack))
                    for e in edge_stack:
                        e[1] -= flow
                        re = self.g[e[0]][e[2]]
                        re[1] += flow
                    return flow

                next_level = level[v] - 1
                for i in range(current_edge[v], len(self.g[v])):
                    e = self.g[v][i]
                    re = self.g[e[0]][e[2]]
                    if level[e[0]] != next_level or not re[1]: continue
                    stack.append(e[0])
                    edge_stack.append(re)
                    break
                else:
                    if edge_stack: edge_stack.pop()
                    level[v] = self.n
                current_edge[v] = i
            return 0

        flow = 0
        while flow < flow_limit:
            level = bfs()
            if level[t] == -1: break
            current_edge = [0] * self.n
            while flow < flow_limit:
                f = dfs(flow_limit - flow)
                if not f: break
                flow += f
        return flow

    def min_cut(self, s: int) -> List[bool]:
        visited = [False] * self.n
        stack = [s]
        visited[s] = True
        while stack:
            v = stack.pop()
            for e_dst, e_cap, e_revidx in self.g[v]:
                if e_cap > 0 and not visited[e_dst]:
                    visited[e_dst] = True
                    stack.append(e_dst)
        return visited
