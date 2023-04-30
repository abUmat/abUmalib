from typing import List
class Binominal:
    def __init__(self, mod: int, max: int=0) -> None:
        self.mod = mod
        self.f = f = [1]
        self.g = [1]
        self.h = [1]
        while max >= len(f): self.extend()

    def extend(self) -> None:
        mod = self.mod
        f, g, h = self.f, self.g, self.h
        n = len(f)
        m = n << 1
        f[n:] = [0] * n
        g[n:] = [0] * n
        h[n:] = [0] * n
        for i in range(n, m): f[i] = f[i - 1] * i % mod
        g[-1] = pow(f[-1], mod - 2, mod)
        h[-1] = g[-1] * f[-2] % mod
        for i in range(m - 2, n - 1, -1):
            g[i] = g[i + 1] * (i + 1) % mod
            h[i] = g[i] * f[i - 1] % mod

    def fac(self, i: int) -> int:
        if i < 0: return 0
        while i >= len(self.f): self.extend()
        return self.f[i]

    def finv(self, i: int) -> int:
        if i < 0: return 0
        while i >= len(self.g): self.extend()
        return self.g[i]

    def inv(self, i: int) -> int:
        if i < 0:
            tmp = pow(-i, self.mod - 2, self.mod)
            if tmp: return self.mod - tmp
            else: return 0
        while i > len(self.h): self.extend()
        return self.h[i]

    def __call__(self, n: int, r: int) -> int:
        return self.C(n, r)

    def multinominal(self, r: List[int]) -> int:
        n = 0
        for x in r:
            if x < 0: return 0
            n += x
        res = self.fac(n)
        mod = self.mod; finv = self.finv
        for x in r: res = res * finv(x) % mod
        return res

    def C_naive(self, n: int, r: int) -> int:
        if n < 0 or n < r or r < 0: return 0
        mod = self.mod
        res = 1
        r = min(r, n - r)
        for i in range(1, r + 1):
            res = (res * pow(i, mod - 2, mod)  % mod) * n
            n -= 1
        return res

    def C(self, n: int, r: int) -> int:
        'nCr'
        if n < 0 or n < r or r < 0: return 0
        return (self.fac(n) * self.finv(n - r) % self.mod) * self.finv(r) % self.mod

    def P(self, n: int, r: int) -> int:
        'nPr'
        if n < 0 or n < r or r < 0: return 0
        return self.fac(n) * self.finv(n - r) % self.mod

    def H(self, n: int, r: int) -> int:
        'nHr'
        if n < 0 or r < 0: return 0
        return self.C(n + r - 1, r) if r else 1

