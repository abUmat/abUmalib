# my module
from data_structure.bit import *
from data_structure.sparse_table import *
# my module
class EulerTour:
    def __init__(self, g, root: int=0) -> None:
        '''
        euler tourを行い初期化
        ete: 通る辺の順番
        etv: 通る頂点の順番
        in_: 頂点を最初に通った時刻
        out: 頂点を最後に通った時刻
        depth: 頂点の深さ
        '''
        self.n = n = len(g)
        ete = []
        etv = []
        parents = [0] * n
        in_ = [0] * n
        out = [0] * n
        depth = [-1] * n
        stack = [root]
        depth[root] = 0
        i = 0
        while stack:
            v = stack.pop()
            if v >= 0:
                stack.append(~v)
                ete.append(v)
                etv.append(v)
                in_[v] = i
                for vv in g[v]:
                    if depth[vv] != -1: continue
                    depth[vv] = depth[v] + 1
                    parents[vv] = v
                    stack.append(vv)
            else:
                ete.append(~v)
                etv.append(parents[~v])
                out[~v] = i
            i += 1
        etv.pop()
        self.ete, self.etv = ete, etv
        self.in_, self.out = in_, out
        self.depth = depth
        self.st = SparseTable([depth[v] << 20 | v for v in etv])

    def build(self, arr: list) -> None:
        '''arrで値を初期化する'''
        arr_for_path = [0] * (self.n << 1)
        for i, e in enumerate(self.ete):
            arr_for_path[i] += arr[e]
            arr[e] = -arr[e]
        self.bit_for_path = BIT(self.n << 1, arr_for_path)

        arr_for_subtree = [0] * (self.n << 1)
        for i, e in enumerate(self.ete):
            arr_for_subtree[i] += arr[e]
            arr[e] = 0
        self.bit_for_subtree = BIT(self.n << 1, arr_for_subtree)

    def lca(self, u: int, v: int) -> int:
        '''LCA of u and v'''
        x, y = self.in_[u], self.in_[v]
        if x > y: x, y = y, x
        res = self.st.query(x, y + 1)
        return res & 0xfffff

    def add(self, p: int, x: int) -> int:
        '''頂点pにxを加える'''
        self.bit_for_path.add(self.in_[p], x)
        self.bit_for_path.add(self.out[p], -x)
        self.bit_for_subtree.add(self.in_[p], x)

    def query_vertex(self, u: int, v: int) -> int:
        '''頂点に値を持つ場合のpath-sum'''
        lca = self.lca(u, v)
        pref = self.bit_for_path.pref
        return pref(self.in_[u] + 1) + pref(self.in_[v] + 1) - (pref(self.in_[lca] + 1) << 1) + self.bit_for_path[self.in_[lca]]

    def query_edge(self, u: int, v: int) -> int:
        '''辺に値を持つ場合のpath-sum'''
        lca = self.lca(u, v)
        pref = self.bit_for_path.pref
        return pref(self.in_[u] + 1) + pref(self.in_[v] + 1) - (pref(self.in_[lca] + 1) << 1)

    def query_subtree(self, u: int) -> int:
        '''頂点uのsubtree-sum'''
        return self.bit_for_subtree.sum(self.in_[u], self.out[u])
