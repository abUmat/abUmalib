# my module
from segment_tree.segment_tree import *
# my module
class LazySegmentTree(SegmentTree):
    def __init__(self, n: int, e: int, id_: int, op: callable, mapping: callable, composition: callable, arr: list=None) -> None:
        '''
        n: length
        e: identity_element of merge
        id_: identity_element of composition
        op: op(x, y) merge function
        mapping: mapping(x, length, F) apply function
        composition: composition(F, G) compositon function F(G)
        '''
        super().__init__(n, e, op, arr)
        self.id = id_
        self.mapping = mapping
        self.composition = composition
        self.lazy = [id_] * self.size

    def _all_apply(self, i: int, F: int) -> None:
        self.data[i] = self.mapping(self.data[i], self.len[i], F)
        if i < self.size: self.lazy[i] = self.composition(F, self.lazy[i])

    def _push(self, i: int) -> None:
        self._all_apply(i << 1 | 0, self.lazy[i])
        self._all_apply(i << 1 | 1, self.lazy[i])
        self.lazy[i] = self.id

    def update(self, k: int, x: int) -> None:
        k += self.size
        for i in range(self.log, 0, -1): self._push(k >> i)
        self.data[k] = x
        for i in range(1, self.log+1): self._update(k >> i)

    def apply(self, k: int, F: int) -> None:
        k += self.size
        for i in range(self.log, 0, -1): self._push(k >> i)
        self.data[k] = self.mapping(self.data[k], self.len[k], F)
        for i in range(1, self.log + 1): self._update(k >> i)

    def range_apply(self, l: int, r: int, F: int) -> None:
        if l == r: return
        l += self.size
        r += self.size
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l: self._push(l >> i)
            if ((r >> i) << i) != r: self._push((r - 1) >> i)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                self._all_apply(l, F)
                l += 1
            if r & 1:
                r ^= 1
                self._all_apply(r, F)
            l >>= 1
            r >>= 1
        l, r = l2, r2
        for i in range(1, self.log + 1):
            if ((l >> i) << i) != l: self._update(l >> i)
            if ((r >> i) << i) != r: self._update((r - 1) >> i)

    def get(self, k: int) -> None:
        k += self.size
        for i in range(self.log, 0, -1): self._push(k>>i)
        return self.data[k]

    def prod(self, l: int, r: int) -> int:
        if l == r: return self.e
        l += self.size
        r += self.size
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l: self._push(l >> i)
            if ((r >> i) << i) != r: self._push((r - 1) >> i)
        sml, smr = self.e, self.e
        while l < r:
            if l & 1:
                sml = self.op(sml, self.data[l])
                l += 1
            if r & 1:
                r ^= 1
                smr = self.op(self.data[r], smr)
            l >>= 1
            r >>= 1
        return self.op(sml, smr)

    def max_right(self, l: int, func: callable) -> int:
        if l == self.n: return self.n
        l += self.size
        for i in range(self.log, 0, -1): self._push(l >> i)
        sm = self.e
        while 1:
            while not l & 1: l >>= 1
            if not func(self.op(sm, self.data[l])):
                while l < self.size:
                    self._push(l)
                    l <<= 1
                    if func(self.op(sm, self.data[l])):
                        sm = self.op(sm, self.data[l])
                        l += 1
                return l - self.size
            sm = self.op(sm, self.data[l])
            l += 1
            if (l & -l) == l: break
        return self.n

    def max_left(self, r: int, func: callable) -> int:
        if r == 0: return 0
        r += self.size
        for i in range(self.log, 0, -1): self._push((r - 1) >> i)
        sm = self.e
        while 1:
            r -= 1
            while r > 1 and r & 1: r >>= 1
            if not func(self.op(self.data[r], sm)):
                while r < self.size:
                    self._push(r)
                    r = r << 1 | 1
                    if func(self.op(self.data[r], sm)):
                        sm = self.op(self.data[r], sm)
                        r ^= 1
                return r + 1 - self.size
            sm = self.op(self.data[r], sm)
            if (r & -r) == r: break
        return 0
