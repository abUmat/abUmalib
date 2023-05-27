class SegmentTree:
    def __init__(self, n: int, e: int, op: callable, arr: list=None):
        self.n = n
        self.log = (n - 1).bit_length()
        self.size = 1 << self.log
        self.e = e
        self.op = op
        self.data = [e] * (self.size << 1)
        self.len = [1] * (self.size << 1)
        if arr:
            self.arr = arr
            self.build()
        else: self.arr = [e] * n

    def _update(self, i: int) -> None:
        self.data[i] = self.op(self.data[i << 1], self.data[i << 1 | 1])

    def build(self) -> None:
        for i, a in enumerate(self.arr, self.size): self.data[i] = a
        for i in range(self.size-1, 0, -1):
            self._update(i)
            self.len[i] = self.len[i << 1] + self.len[i << 1 | 1]

    def update(self, k: int, x: int) -> None:
        k += self.size
        self.data[k] = x
        for i in range(1, self.log + 1): self._update(k >> i)

    def add(self, k: int, x: int) -> None:
        k += self.size
        self.data[k] += x
        for i in range(1, self.log + 1): self._update(k >> i)

    def set(self, k: int, x: int) -> None:
        self.arr[k] = x

    def get(self, k: int) -> int:
        return self.data[k + self.size]

    def prod(self, l: int, r: int) -> int:
        sml, smr = self.e, self.e
        l += self.size
        r += self.size
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

    def all_prod(self) -> int:
        return self.data[1]
