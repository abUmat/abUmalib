from bisect import bisect_left as lower_bound
class BITRangeTree:
    class BIT:
        def __init__(self, size: int) -> None:
            self.N = size
            self.data = [0] * (size + 1)

        def add(self, k: int, x: int) -> None:
            k += 1
            while k <= self.N:
                self.data[k] += x
                k += k & -k

        def pref(self, k: int) -> int:
            res = 0
            while k:
                res += self.data[k]
                k ^= k & -k
            return res

        def sum(self, l: int, r: int) -> int:
            res = 0
            while l != r:
                if l < r:
                    res += self.data[r]
                    r ^= r & -r
                else:
                    res -= self.data[l]
                    l ^= l & -l
            return res

    ps = []

    def add_point(self, x: int, y: int) -> None:
        'add point (x, y) for initialize'
        self.ps.append(x << 30 | y)
        # self.ps.append((x, y))

    def build(self) -> None:
        'initialize'
        mask = (1 << 30) -1
        BIT = self.BIT
        self.ps = ps = sorted(set(self.ps))
        self.xs = [p >> 30 for p in ps]
        self.N = N = len(ps)
        self.ys = ys = [[] for _ in range(N + 1)]
        for i in range(N + 1):
            j = i + 1
            while j <= N:
                ys[j].append(ps[i] & mask)
                j += j & -j
            ys[i] = sorted(set(ys[i]))
        self.bit = [BIT(len(y)) for y in ys]

    def add(self, x: int, y: int, a: int) -> None:
        'add value to point (x, y)'
        i = lower_bound(self.ps, x << 30 | y)
        i += 1
        bit = self.bit; ys = self.ys
        while i <= self.N:
            bit[i].add(lower_bound(ys[i], y), a)
            i += i & -i

    def _sum(self, x: int, y: int) -> int:
        res = 0
        a = lower_bound(self.xs, x)
        bit = self.bit; ys = self.ys
        while a:
            res += bit[a].pref(lower_bound(ys[a], y))
            a ^= a & -a
        return res

    def sum(self, xl: int, yl: int, xr: int, yr: int) -> int:
        'sum of rectangle [(xl, yl), (xr, yr))'
        res = 0
        a = lower_bound(self.xs, xl); b = lower_bound(self.xs, xr)
        bit = self.bit; ys = self.ys
        while a != b:
            if a < b:
                res += bit[b].sum(lower_bound(ys[b], yl), lower_bound(ys[b], yr))
                b ^= b & -b
            else:
                res -= bit[a].sum(lower_bound(ys[a], yl), lower_bound(ys[a], yr))
                a ^= a & -a
        return res
