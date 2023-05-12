from collections import deque
# my module
from tree.centroid_decomposition import *
from ntt.arbitrary_ntt import *
# my module
class FrequencyTableOfTreeDistance(CentroidDecomposition):
    def __init__(self, g) -> None:
        super().__init__(g, 0)

    def _dfs_depth(self, cur: int, par: int, d: int, count: List[int], self_: List[int]) -> None:
        mask = (1 << 20) - 1
        q = [cur << 40 | par << 20 | d]
        while q:
            x = q.pop()
            cur, par, d = x >> 40, x >> 20 & mask, x & mask
            count[len(count):] = [0] * (d + 1 - len(count))
            self_[len(self_):] = [0] * (d + 1 - len(self_))
            count[d] += 1
            self_[d] += 1
            for dst in self.g[cur]:
                if par == dst or self.v[dst]: continue
                q.append(dst << 40 | cur << 20 | (d + 1))

    def get(self, start: int=0) -> List[int]:
        pow2 = ArbitraryNTT.pow2_u128
        get_centroid, get_size = self.get_centroid, self.get_size
        Q: deque[int] = deque()
        root = get_centroid(start, get_size(start) >> 1)
        Q.append(root)
        ans: List[int] = [0] * (len(self.g) + 1)
        while Q:
            r = Q.popleft()
            count = []
            self.v[r] = 1
            for c in self.g[r]:
                if self.v[c]: continue
                self_ = []
                Q.append(get_centroid(c, get_size(c) >> 1))
                self._dfs_depth(c, r, 1, count, self_)
                self2 = pow2(self_)
                for i, x in enumerate(self2): ans[i] -= x
            if not count: continue
            count[0] += 1
            count2 = pow2(count)
            for i, x in enumerate(count2): ans[i] += x
        for i in range(len(ans)): ans[i] >>= 1
        return ans

