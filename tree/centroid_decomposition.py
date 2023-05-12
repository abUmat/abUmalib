class CentroidDecomposition:
    def __init__(self, G, isbuild=1) -> None:
        self.g = G
        self.sub = [0] * len(G)
        self.v = bytearray(len(G))
        if isbuild: self.build()

    def build(self) -> None:
        self.tree = [[] for _ in range(len(self.g))]
        self.root = self.build_dfs(0)

    def get_size(self, _cur: int, _par: int) -> int:
        q = [[_cur, _par]]
        while q:
            cur, par = q.pop()
            if cur >= 0:
                q.append([~cur, par])
                self.sub[cur] = 1
                for dst in self.g[cur]:
                    if dst == par or self.v[dst]: continue
                    q.append([dst, cur])
            else:
                if par == -1: return self.sub[~cur]
                self.sub[par] += self.sub[~cur]

    def get_centroid(self, _cur: int, _par: int, mid: int) -> int:
        q = [[_cur, _par]]
        ans = -1
        while q:
            cur, par = q.pop()
            if cur >= 0:
                q.append([~cur, par])
                for dst in self.g[cur]:
                    if dst == par or self.v[dst]: continue
                    if self.sub[dst] > mid:
                        q.append([dst, cur])
                        break
            else:
                if ans == -1: ans = ~cur
                if par == -1: return ans

    def build_dfs(self, cur: int) -> int:
        centroid = self.get_centroid(cur, -1, self.get_size(cur, -1) >> 1)
        self.v[centroid] = 1
        for dst in self.g[centroid]:
            if not self.v[dst]:
                nxt = self.build_dfs(dst)
                if centroid != nxt: self.tree[centroid].append(nxt)
        self.v[centroid] = 0
        return centroid
