# my module
from misc.typing_template import *
# my module
# https://judge.yosupo.jp/submission/97236
# https://nyaannyaan.github.io/library/tree/heavy-light-decomposition.hpp
class HeavyLightDecomposition:
    def __init__(self, g: Graph, root: int=0) -> None:
        n = len(g)
        parent = [-1] * n
        order = [root] # bfs-order
        # memo bfs-order, parent
        for i, p in enumerate(order):
            pp = parent[p]
            for e in g[p]:
                if pp != e:
                    order.append(e)
                    parent[e] = p

        # calc size and memo heavy-child by post-order
        size = [1] * n
        heavy_child = [-1] * n
        for i in range(n - 1, 0, -1):
            p = order[i]
            size[parent[p]] += size[p]
            if heavy_child[parent[p]] == -1: heavy_child[parent[p]] = p
            if size[heavy_child[parent[p]]] < size[p]: heavy_child[parent[p]] = p

        # memo heavy-parent
        heavy_root = list(range(n))
        for p in order:
            if heavy_child[p] != -1:
                heavy_root[heavy_child[p]] = p

        # calc depth and'HLD-tree depth', memo heavy-root
        hld_depth = [n] * n
        hld_depth[root] = 0
        depth = [0] * n
        for p in order:
            if p != root:
                heavy_root[p] = heavy_root[heavy_root[p]]
                hld_depth[p] = min(hld_depth[heavy_root[p]], hld_depth[parent[p]] + 1)
                depth[p] = depth[parent[p]] + 1

        # memo down(:= in) and up(:= out) like euler tour
        down = [0] * n
        up = [0] * n
        for p in order:
            up[p] = down[p] + size[p]
            ir = up[p]
            for e in g[p]:
                if parent[p] != e and e != heavy_child[p]:
                    ir -= size[e]
                    down[e] = ir
                if heavy_child[p] != -1:
                    down[heavy_child[p]] = down[p] + 1

        # change order from bfs-order to dfs-order
        for i, idx in enumerate(down): order[idx] = i

        self.n = n
        self.parent = parent
        self.depth = depth
        self.size = size
        self.ord = order
        self.heavy_root = heavy_root
        self.heavy_child = heavy_child
        self.hld_depth = hld_depth
        self.down = down
        self.up = up

    def lca(self, u: int, v: int) -> int:
        parent, d, p = self.parent, self.hld_depth, self.heavy_root
        if d[u] < d[v]: u, v = v, u
        while d[u]  > d[v]: u = parent[p[u]]
        while p[u] != p[v]: u, v = parent[p[u]], parent[p[v]]
        return v if self.depth[u] > self.depth[v] else u

    def dist(self, u: int, v: int) -> int:
        return self.depth[u] + self.depth[v] - (self.depth[self.lca(u, v)] << 1)

    def path(self, r: int, c: int, include_root: bool=1, reverse: bool=0) -> List[Tuple[int, int]]:
        '''
        return: [(l0, r0), (l1, r1)...] s.t. path(r, c) == ord[l0, r0) + ord[l1, r1) + ...
        '''
        parent, d, p = self.parent, self.hld_depth, self.heavy_root
        if d[c] < d[r]: return []
        res: List[Tuple[int, int]] = [0] * (d[c] - d[r] + 1)
        for i in range(len(res) - 1):
            res[i] = self.down[p[c]], self.down[c] + 1
            c = parent[p[c]]
        if p[r] != p[c] or self.depth[r] > self.depth[c]: return []
        res[-1] = self.down[r] + int(not include_root), self.down[c] + 1
        if res[-1][0] == res[-1][1]: res.pop()
        if not reverse:
            res.reverse()
        else:
            for i, (a, b) in enumerate(res):
                res[i] = b, a
        return res

    def subtree(self, p: int) -> Tuple[int, int]:
        return self.down[p], self.up[p]

    def la(self, frm: int, to: int, d: int) -> int:
        if d < 0: return -1
        lca = self.lca(frm, to)
        dist0 = self.depth[frm] + self.depth[to] - (self.depth[lca] << 1)
        if dist0 < d: return -1
        p = frm
        if self.depth[frm] - self.depth[lca] < d:
            p = to
            d = dist0 - d
        while self.depth[p] - self.depth[self.heavy_root[p]] < d:
            d -= self.depth[p] - self.depth[self.heavy_root[p]] + 1
            p = self.parent[self.heavy_root[p]]
        return self.ord[self.down[p] - d]

    def path_query(self, u: int, v: int, vertex: bool, f: Func20) -> None:
        lca = self.lca(u, v)
        for l, r in self.path(lca, u, 0): f(l, r)
        if vertex: f(self.down[lca], self.down[lca] + 1)
        for l, r in self.path(lca, v, 0): f(l, r)

    def path_noncommutative_query(self, u: int, v: int, vertex: bool, f: Func20) -> None:
        lca = self.lca(u, v)
        for l, r in self.path(lca, u, 0, 1): f(l, r)
        if vertex: f(self.down[lca], self.down[lca] + 1)
        for l, r in self.path(lca, v, 0): f(l, r)

    def subtree_query(self, u: int, vertex: bool, f: Func20) -> None:
        f(self.down[u] + int(not vertex), self.up[u])
