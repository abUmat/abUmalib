from typing import List, Callable
class Rerooting:
    def __init__(self, g: List[List[int]], f1: Callable[[int, int], int], f2: Callable[[int, int, int], int], e: int, arr: List[int]=None) -> None:
        '''
        g: Graph
        f1: f1(c1, c2) merge value of child node
        f2: f2(memo[i], chd, par) value from child node to parent node
        e: identity_element of f1 and f2
        arr: List of node values
        '''
        self.g = g
        self.f1 = f1
        self.f2 = f2
        if not arr: arr = [e] * len(g)
        self._memo = arr[:]
        self.dp = arr[:]
        self.e = e
        self._dfs(0, 0)
        self._efs(0, -1, e)

    def __getitem__(self, k: int):
        return self.dp[k]

    def _dfs(self, v: int, par: int) -> None:
        mask = (1 << 20) - 1
        f1, f2 = self.f1, self.f2
        g, memo = self.g, self._memo
        q = [1 << 40 | v << 20 | par]
        while q:
            x = q.pop()
            flg, v, par = x >> 40, x >> 20 & mask, x & mask
            if flg:
                q.append(v << 20 | par)
                for vv in g[v]:
                    if vv == par: continue
                    q.append(1 << 40 | vv << 20 | v)
            else:
                if par: memo[par] = f1(memo[par], f2(memo[v], v, par))

    def _efs(self, v: int, par: int, pval: int) -> None:
        f1, f2, e = self.f1, self.f2, self.e
        g, memo, dp = self.g, self._memo, self.dp
        q = [[v, par, pval]]
        while q:
            v, par, pval = q.pop()
            buf: List[int] = []
            for vv in g[v]:
                if vv == par: continue
                buf.append(f2(memo[vv], vv, v))
            n = len(buf)
            head = [0] * (n + 1)
            tail = [0] * (n + 1)
            head[0] = h = dp[v]
            tail[0] = t = e
            for i, x in enumerate(buf):
                head[i + 1] = h = f1(h, x)
                tail[i + 1] = t = f1(t, buf[-i - 1])

            # update
            dp[v] = h if par == -1 else f1(pval, h)

            # propagate
            idx = 0
            for vv in g[v]:
                if vv == par: continue
                q.append([vv, v, f2(f1(pval, f1(head[idx], tail[-idx - 2])), v, vv)])
                idx += 1
