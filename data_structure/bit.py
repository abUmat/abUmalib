class BIT:
    """
    n: size
    data: Iterable
    """
    def __init__(self, size: int, data=None) -> None:
        self.N = size + 2
        self.data = [0] * (size + 3)
        self.all = 0
        if data:
            for i, a in enumerate(data):
                self.add(i, a)

    def add(self, k: int, x: int) -> None:
        self.all += x
        k += 1
        while k <= self.N:
            self.data[k] += x
            k += k & -k

    def imos(self, l: int, r: int, x: int) -> None:
        self.add(l, x)
        self.add(r + 1, -x)

    def pref(self, k: int) -> int:
        """sum of [0, k)"""
        if k <= 0: return 0
        res = 0
        while k > 0:
            res += self.data[k]
            k &= k - 1
        return res

    def suff(self, k: int) -> int:
        """sum of [k, n)"""
        return self.all - self.pref(k)

    def sum(self, l: int, r: int) -> int:
        """sum of [l, r)"""
        return self.pref(r) - self.pref(l)

    def __getitem__(self, k: int) -> int:
        return self.pref(k+1) - self.pref(k)

    def lower_bound(self, w: int) -> int:
        """minimize i s.t. pref(i) >= w"""
        if w <= 0: return 0
        x = 0
        k = 1<<(self.N.bit_length()-1)
        while k:
            if x + k <= self.N and self.data[x + k] < w:
                w -= self.data[x + k]
                x += k
            k >>= 1
        return x + 1

    def upper_bound(self, w: int) -> int:
        """minimize i s.t. pref(i) > w"""
        if w < 0: return 0
        x = 0
        k = 1<<(self.N.bit_length()-1)
        while k:
            if x + k <= self.N and self.data[x + k] <= w:
                w -= self.data[x + k]
                x += k
            k >>= 1
        return x + 1

def inversion_number(arr):
    inv = {a:i for i, a in enumerate(sorted(set(arr)))}
    compressed = [inv[a] for a in arr]
    bit = BIT(len(inv))
    res = 0
    for a in compressed:
        res += bit.suff(a + 1)
        bit.add(a, 1)
    return res
