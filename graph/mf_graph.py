# my module
from misc.typing_template import *
# my module
class MFGraph:
    def edge_zip(self, cap: int, dst: int, idx: int) -> int:
        return cap << 40 | dst << 20 | idx

    def __init__(self, n: int) -> None:
        self._n = n
        self._g: List[List[int]] = [[] for _ in range(n)]
        self._edges: List[int] = []
        self.idx = 0

    def add_edge(self, src: int, dst: int, cap: int) -> int:
        assert 0 <= src < self._n
        assert 0 <= dst < self._n
        assert 0 <= cap
        # e := cap << 40 | dst << 20 | index of reverse edge in self._edges
        e = self.edge_zip(cap, dst, self.idx + 1)
        re = self.edge_zip(0, src, self.idx)
        self._g[src].append(self.idx)
        self._g[dst].append(self.idx + 1)
        self._edges.append(e)
        self._edges.append(re)
        self.idx += 2
        return self.idx >> 1


    def get_edge(self, i: int, unpack: bool=0) -> Union[Pair, Tuple[int, int, int, int]]:
        '''
        unpack is true: tuple(src, dst, cap, flow)
        unpack is false: tuple(flow << 20 | src, cap << 20 | dst)
        '''
        i <<= 1
        assert 0 <= i < len(self._edges)
        tmp = self._edges[i]
        cap_dst, revidx = tmp >> 20, tmp & 0xfffff
        rcap_rdst = self._edges[revidx] >> 20
        if unpack: return rcap_rdst & 0xfffff, cap_dst & 0xfffff, cap_dst + rcap_rdst >> 20, rcap_rdst >> 20
        return rcap_rdst, cap_dst + (rcap_rdst & 0xfffff00000)

    def edges(self, unpack: bool=0) -> List[Union[Pair, Tuple[int, int, int, int]]]:
        '''
        unpack is true: list of tuple(src, dst, cap, flow)
        unpack is false: list of tuple(flow << 20 | src, cap << 20 | dst)
        '''
        if unpack:
            ret = [self.get_edge(i) for i in range(len(self._edges) >> 1)]
            return [(flow_src & 0xfffff, cap_dst & 0xfffff, cap_dst >> 20, flow_src >> 20) for flow_src, cap_dst in ret]
        return [self.get_edge(i) for i in range(len(self._edges) >> 1)]

    def change_edge(self, i: int, new_cap: int, new_flow: int) -> None:
        assert 0 <= i < len(self._edges)
        assert 0 <= new_flow <= new_cap
        tmp = self._edges[i]
        revidx = tmp & 0xfffff
        self._edges[i] = self.edge_zip(new_cap - new_flow, tmp & 0xfffff00000, revidx)
        self._edges[revidx] = new_flow << 40 | (self._edges[revidx] & 0xffffffffff)

    def flow(self, s: int, t: int, flow_limit: Optional[int] = None) -> int:
        assert 0 <= s < self._n
        assert 0 <= t < self._n
        assert s != t
        if flow_limit is None:
            flow_limit = sum(self._edges[idx] >> 40 for idx in self._g[s])

        current_edge = [0] * self._n
        level = [0] * self._n

        def fill(arr: List[int], value: int) -> None:
            for i in range(len(arr)):
                arr[i] = value

        def bfs() -> bool:
            fill(level, self._n)
            queue = [s]
            level[s] = 0
            for v in queue:
                next_level = level[v] + 1
                for idx in self._g[v]:
                    cap_dst = self._edges[idx] >> 20
                    cap, dst = cap_dst >> 20, cap_dst & 0xfffff
                    if cap == 0 or level[dst] <= next_level:
                        continue
                    level[dst] = next_level
                    if dst == t:
                        return 1
                    queue.append(dst)
            return 0

        def dfs(lim: int) -> int:
            stack = []
            edge_stack: List[int] = []
            stack.append(t)
            while stack:
                v = stack[-1]
                if v == s:
                    flow = min(lim, min(self._edges[idx] >> 40 for idx in edge_stack))
                    for idx in edge_stack:
                        self._edges[idx] -= flow << 40
                        self._edges[self._edges[idx] & 0xfffff] += flow << 40
                    return flow
                next_level = level[v] - 1
                gv = self._g[v]
                leng = len(gv)
                while current_edge[v] < leng:
                    idx = gv[current_edge[v]]
                    dst_revidx = self._edges[idx] & 0xffffffffff
                    dst, revidx = dst_revidx >> 20, dst_revidx & 0xfffff
                    if level[dst] != next_level or not self._edges[revidx] >> 40:
                        current_edge[v] += 1
                        continue
                    stack.append(dst)
                    edge_stack.append(revidx)
                    break
                else:
                    stack.pop()
                    if edge_stack:
                        edge_stack.pop()
                    level[v] = self._n
            return 0

        flow = 0
        while flow < flow_limit:
            if not bfs():
                break
            fill(current_edge, 0)
            while flow < flow_limit:
                f = dfs(flow_limit - flow)
                if f: flow += f
                else: break
        return flow

    def min_cut(self, s: int) -> List[bool]:
        visited = bytearray(self._n)
        stack = [s]
        visited[s] = 1
        while stack:
            v = stack.pop()
            for e in self._g[v]:
                cap, dst = e >> 40, e >> 20 & 0xfffff
                if cap > 0 and not visited[dst]:
                    visited[dst] = 1
                    stack.append(dst)
        return visited

