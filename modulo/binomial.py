# my module
from modulo.modinv import *
# my module
# https://nyaannyaan.github.io/library/modulo/binomial.hpp
class Binomial:
    def __init__(self, mod: int, max_length=10_001_000) -> None:
        if max_length < 2: max_length = 2
        self.mod = mod
        self.f = f = [0] * max_length
        self.g = g = [0] * max_length
        self.h = h = [0] * max_length
        f[0] = g[0] = h[0] = tmp = 1
        for i in range(1, max_length): f[i] = tmp = tmp * i % mod
        g[-1] = tmp = modinv(f[-1], mod)
        h[-1] = tmp * f[-2] % mod
        for i in range(max_length - 2, 0, -1):
            g[i] = tmp = tmp * (i + 1) % mod
            h[i] = tmp * f[i - 1] % mod

    def extend(self) -> None:
        mod = self.mod
        f, g, h = self.f, self.g, self.h
        n = len(f)
        tmpf = f[-1]
        m = n << 1
        f[n:] = [0] * n
        g[n:] = [0] * n
        h[n:] = [0] * n
        for i in range(n, m): f[i] = tmpf = tmpf * i % mod
        g[-1] = tmpg = modinv(tmpf, mod)
        h[-1] = tmpg * f[-2] % mod
        for i in range(m - 2, n - 1, -1):
            g[i] = tmpg = tmpg * (i + 1) % mod
            h[i] = tmpg * f[i - 1] % mod

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
            tmp = modinv(-i, self.mod)
            if tmp: return self.mod - tmp
            else: return 0
        while i > len(self.h): self.extend()
        return self.h[i]


    def __call__(self, n: int, r: int) -> int:
        return self.C(n, r)

    def multinominal(self, r: list) -> int:
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
            res = (res * modinv(i, mod)  % mod) * n % mod
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
