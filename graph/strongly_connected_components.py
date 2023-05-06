import sys
# https://qiita.com/AkariLuminous/items/a2c789cebdd098dcb503
def csr(n, E):
    start = [0] * (n + 1)
    elist = [0] * len(E)
    # start[i+1] = 頂点 i を始点とする辺の数
    for e0, e1 in E:
        start[e0 + 1] += 1
    #累積和
    for i in range(1, n + 1):
        start[i] += start[i - 1]
    #挿入位置を表すポインタ
    counter = start[:]
    for e0, e1 in E:
        elist[counter[e0]] = e1
        counter[e0] += 1 # ポインタを進める
    return start, elist

class SCC:
    def __init__(self, n):
        self._n = n
        self.edges = []
        sys.setrecursionlimit(max(2*n, sys.getrecursionlimit()))

    def num_vertices(self): return self._n

    def add(self, frm, to): self.edges.append([frm, to])

    def scc(self):
        group_num, ids = self.scc_ids()
        groups = [[] for _ in range(group_num)]
        for i in range(self._n): groups[ids[i]].append(i)
        return groups

    def scc_ids(self):
        start, elist = csr(self._n, self.edges)
        now_ord, group_num = 0, 0
        visited = []
        low = [0] * self._n
        ord_ = [-1] * self._n
        ids = [0] * self._n

        def dfs(v):
            nonlocal now_ord, group_num, visited, low, ord_, ids
            low[v] = ord_[v] = now_ord
            now_ord += 1
            visited.append(v)
            for i in range(start[v], start[v+1]):
                to = elist[i]
                if ord_[to] == -1:
                    dfs(to)
                    low[v] = min(low[v], low[to])
                else:
                    low[v] = min(low[v], ord_[to])
            if low[v] == ord_[v]:
                while True:
                    u = visited.pop()
                    ord_[u] = self._n
                    ids[u] = group_num
                    if u == v: break
                group_num += 1

        for i in range(self._n):
            if ord_[i] == -1: dfs(i)
        for i in range(self._n): ids[i] = group_num - 1 - ids[i]
        return group_num, ids
