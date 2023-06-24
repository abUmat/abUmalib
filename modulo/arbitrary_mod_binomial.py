# my module
from misc.typing_template import *
# my module
# https://nyaannyaan.github.io/library/modulo/arbitrary-mod-binomial.hpp
class _PrimePowerBinomial:
    N_MAX = 20000000
    M_MAX = (1<<30)-1
    def __init__(self, _p: int, _q: int) -> None:
        self.p, self.q = _p, _q
        m = 1
        for _ in range(_q): m *= self.p
        self.M = m
        self.mask = self.M - 1
        self.delta = 1 if self.p == 2 and self.q >= 3 else -1
        # 前計算
        MX = min(self.M, self.N_MAX + 10)
        self.fac = [0] * MX
        self.ifac = [0] * MX
        self.inv = [0] * MX
        self.fac[0] = self.ifac[0] = self.inv[0] = 1
        self.fac[1] = self.ifac[1] = self.inv[1] = 1
        i = 2
        while i < MX:
            if i%self.p:
                self.fac[i] = self.fac[i-1] * i % self.M
            else:
                self.fac[i] = self.fac[i-1]
                self.fac[i+1] = self.fac[i-1] * (i+1) % self.M
                i += 1
            i += 1
        self.ifac[MX-1] = pow(self.fac[-1], self.M // self.p * (self.p - 1) - 1, self.M)
        i = MX-2
        while i > 1:
            if i%self.p:
                self.ifac[i] = self.ifac[i+1] * (i+1) % self.M
            else:
                self.ifac[i] = self.ifac[i+1] * (i+1) % self.M
                self.ifac[i-1] = self.ifac[i]
                i -= 1
            i -= 1

    def C(self, n: int, m: int) -> int:
        if n < m or n < 0 or m < 0: return 0
        p = self.p
        # Lucasの定理
        if self.q == 1:
            res = 1
            while n:
                n, n0 = divmod(n, p)
                m, m0 = divmod(m, p)
                if n0 < m0: return 0
                res = res * self.fac[n0] % self.M
                buf = self.ifac[n0-m0] * self.ifac[m0] % self.M
                res = res * buf % self.M
            return res
        r = n-m
        e0, eq, i = 0, 0, 0
        res = 1
        if p == 2:
            while n:
                res = res * self.fac[n& self.mask] & self.mask
                res = res * self.ifac[m& self.mask] & self.mask
                res = res * self.ifac[r& self.mask] & self.mask
                n >>= 1
                m >>= 1
                r >>= 1
                eps = n-m-r
                e0 += eps
                if e0 >= self.q: return 0
                i += 1
                if i >= self.q: eq += eps
            if eq & 1: res = res  * self.delta & self.mask
            res = res * pow(p, e0, self.M) & self.mask
        else:
            M = self.M
            while n:
                res = res * self.fac[n%M] % M
                res = res * self.ifac[m%M] % M
                res = res * self.ifac[r%M] % M
                n = n//p
                m = m//p
                r = r//p
                eps = n-m-r
                e0 += eps
                if e0 >= self.q: return 0
                i += 1
                if i >= self.q: eq += eps
            if eq & 1: res = res  * self.delta % M
            res = res * pow(p, e0, M) % M
        return res

class ArbitraryModBinomial:
    @staticmethod
    def _crt(V: List[Pair]) -> Pair:
        def extgcd(a: int, b: int) -> Pair:
            if b:
                d, y, x = extgcd(b, a % b)
                y -= (a // b) * x
                return d, x, y
            return a, 1, 0
        x = 0; d = 1
        for X, Y in V:
            g, a, b = extgcd(d, Y)
            x, d = (Y*b*x + d*a*X) // g, d*(Y // g)
            x %= d
        return x, d

    def __init__(self, mod: int) -> None:
        self.mod = mod
        self.M = []
        self.cs = []
        for i in range(2, mod):
            if i*i > mod: break
            if not mod%i:
                j, k = 0, 1
                while not mod%i:
                    mod //= i
                    j += 1
                    k *= i
                self.M.append(k)
                self.cs.append(_PrimePowerBinomial(i, j))
        if mod != 1:
            self.M.append(mod)
            self.cs.append(_PrimePowerBinomial(mod, 1))

    def __call__(self, n: int, m: int) -> int:
        '''return: nCm'''
        if self.mod == 1: return 0
        V = []
        for i in range(len(self.cs)):
            V.append((self.cs[i].C(n, m), self.M[i]))
        return self._crt(V)[0]
