from bisect import bisect_left as lower_bound
# https://nyaannyaan.github.io/library/data-structure-2d/abstract-range-tree.hpp
class RangeTree:
    '''
    init -> add_point -> build -> add -> sum
    '''
    def __init__(self, nw: callable, ad: callable, sm: callable, mrg: callable, ti: int) -> None:
        """
        nw: return new data_structure
        ad: data_structre.add(i, a)
        sm: data_structure.sum(l, r)
        mrg: operator merge
        ti: identity element of mrg
        """
        self.ds_new = nw
        self.ds_add = ad
        self.ds_sum = sm
        self.t_merge = mrg
        self.ti = ti
        self.ps = []

    def add_point(self, x: int, y: int) -> None:
        'add point (x, y) for initialize'
        self.ps.append(x << 30 | y)
        # self.ps.append((x, y))

    def build(self) -> None:
        'initialize'
        mask = (1 << 30) -1
        self.ps = ps = sorted(set(self.ps))
        self.xs = [p >> 30 for p in ps]
        ds_new = self.ds_new
        self.N = N = len(ps)
        self.ds = ds = [0] * (N << 1)
        self.ys = ys = [0] * (N << 1)
        ys[N:] = [[p & mask] for p in ps]
        for i in range(1, N)[::-1]: ys[i] = sorted(set(ys[i << 1] + ys[i << 1 | 1]))
        ds[1:N] = [ds_new(len(y)) for y in ys[1:N]]
        ds[N:] = [ds_new(1) for _ in range(N)]

    def add(self, x: int, y: int, a: int) -> None:
        'add value to point (x, y)'
        ds_add = self.ds_add; ds = self.ds; ys = self.ys
        i = lower_bound(self.ps, x << 30 | y)
        i += self.N
        while i:
            ds_add(ds[i], lower_bound(ys[i], y), a)
            i >>= 1

    def sum(self, xl: int, yl: int, xr: int, yr: int) -> int:
        'sum of rectangle [(xl, yl), (xr, yr))'
        t_merge = self.t_merge; ds_sum = self.ds_sum; ds = self.ds; ys = self.ys
        L = self.ti; R = self.ti
        a = lower_bound(self.xs, xl); b = lower_bound(self.xs, xr)
        a += self.N; b += self.N
        while a < b:
            if a & 1:
                L = t_merge(L, ds_sum(ds[a], lower_bound(ys[a], yl), lower_bound(ys[a], yr)))
                a += 1
            if b & 1:
                b ^= 1
                R = t_merge(ds_sum(ds[b], lower_bound(ys[b], yl), lower_bound(ys[b], yr)), R)
            a >>= 1
            b >>= 1
        return t_merge(L, R)
