# my module
from gcc_builtins import *
from misc.typing_template import *
# my module
# https://nyaannyaan.github.io/library/data-structure-2d/wavelet-matrix.hpp
class _BitVector:
    def get(self, i: int) -> int:
        return self.block[i >> 5] >> (i & 31) & 1

    def set(self, i: int) -> int:
        self.block[i >> 5] |= 1 << (i & 31)

    def __init__(self, n: int) -> None:
        self.n = n
        self.zeros = n
        self.block = [0] * ((n >> 5) + 1)
        self.count = [0] * ((n >> 5) + 1)

    def build(self) -> None:
        for i in range(self.n >> 5): self.count[i + 1] = self.count[i] + popcount(self.block[i])
        self.zeros -= self.n - self.rank0(self.n)

    def rank0(self, i: int) -> int:
        return i - self.count[i >> 5] - popcount(self.block[i >> 5] & ((1 << (i & 31)) - 1))

    def rank1(self, i: int) -> int:
        return self.count[i >> 5] - popcount(self.block[i >> 5] & ((1 << (i & 31)) - 1))

class WaveletMatrix:
    isbuilt = 0
    def __init__(self, n: int, arr: list=None, build: bool=True) -> None:
        self.n = n
        if arr: self.arr = arr
        else: self.arr = [0] * n
        if arr and build: self.build()

    def build(self) -> None:
        if self.isbuilt: return
        self.arr = self.arr
        self.n = n = len(self.arr)
        self.lg = lg = max(max(self.arr, default=0), 1).bit_length()
        self.bv = [_BitVector(n) for _ in range(lg)]
        cur = self.arr[::]
        nxt = [0] * n
        for h in range(lg)[::-1]:
            for i in range(n):
                if cur[i] >> h & 1: self.bv[h].set(i)
            self.bv[h].build()
            it = [0, self.bv[h].zeros]
            for i, a in enumerate(cur):
                tmp = self.bv[h].get(i)
                nxt[it[tmp]] = a
                it[tmp] += 1
            cur = nxt[::]
        self.isbuilt = 1

    def set(self, i: int, x: int) -> None:
        'assign x to arr[i]'
        assert(self.isbuilt == 0)
        self.arr[i] = x

    def access(self, k: int) -> int:
        'arr[i]'
        res = 0
        for h in range(self.lg)[::-1]:
            f = self.bv[h].get(k)
            res |= 1<<h if f else 0
            k = k - self.bv[h].rank0(k) + self.bv[h].zeros if f else self.bv[h].rank0(k)
        return res

    def kth_smallest(self, l: int, r: int, k: int) -> int:
        'kth smallest number in [l, r)'
        res = 0
        for h in range(self.lg)[::-1]:
            l0, r0 = self.bv[h].rank0(l), self.bv[h].rank0(r)
            if k < r0 - l0:
                l = l0
                r = r0
            else:
                k -= r0 - l0
                res |= 1<<h
                l += self.bv[h].zeros - l0
                r += self.bv[h].zeros - r0
        return res

    def kth_largest(self, l: int, r: int, k: int) -> int:
        'kth largest number in [l, r)'
        return self.kth_smallest(l, r, r - l - k - 1)

    def pref_freq(self, l: int, r: int, upper: int) -> int:
        'the number of x in [l, r) s.t. x < upper'
        if upper >= 1 << self.lg: return r-l
        res = 0
        for h in range(self.lg)[::-1]:
            f = upper >> h & 1
            l0, r0 = self.bv[h].rank0(l), self.bv[h].rank0(r)
            if f:
                res += r0-l0
                l += self.bv[h].zeros - l0
                r += self.bv[h].zeros - r0
            else:
                l, r = l0, r0
        return res

    def range_freq(self, l: int, r: int, lower: int, upper: int) -> int:
        'the number of x in [l, r) s.t. lower <= x < upper'
        return self.pref_freq(l, r, upper) - self.pref_freq(l, r, lower)

    def prev_value(self, l: int, r: int, upper: int) -> int:
        'the maximan x in [l, r) s.t. x < upper'
        cnt = self.pref_freq(l, r, upper)
        return self.kth_smallest(l, r, cnt-1) if cnt else -1

    def next_value(self, l: int, r: int, lower: int) -> int:
        'the minimum x in [l, r) s.t. x >= lower'
        cnt = self.pref_freq(l, r, lower)
        return -1 if cnt == r-l else self.kth_smallest(l, r, cnt)
