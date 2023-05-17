class Binomial:
    def __init__(self, mod: int, max_length=10_000_000) -> None:
        if max_length < 2: max_length = 2
        self.mod = mod
        self.f = f = [0] * max_length
        self.g = g = [0] * max_length
        self.h = h = [0] * max_length
        f[0] = g[0] = h[0] = tmp = 1
        for i in range(1, max_length): f[i] = tmp = tmp * i % mod
        g[-1] = tmp = pow(f[-1], mod - 2, mod)
        h[-1] = tmp * f[-2] % mod
        for i in range(max_length - 2, 0, -1):
            g[i] = tmp = tmp * (i + 1) % mod
            h[i] = tmp * f[i - 1] % mod

    def fac(self, i: int) -> int:
        return 0 if i < 0 else self.f[i]

    def finv(self, i: int) -> int:
        return 0 if i < 0 else self.g[i]

    def inv(self, i: int) -> int:
        if i < 0:
            tmp = pow(-i, self.mod - 2, self.mod)
            if tmp: return self.mod - tmp
            else: return 0
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
            res = (res * pow(i, mod - 2, mod)  % mod) * n % mod
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

