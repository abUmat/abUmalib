# my module
from math998244353.ntt import *
# my module
# https://nyaannyaan.github.io/library/fps/formal-power-series.hpp
class FPS:
    @staticmethod
    def shrink(a: list) -> None:
        while a and not a[-1]: a.pop()

    @staticmethod
    def resize(a: list, length: int, val: int=0) -> None:
        a[length:] = []
        a[len(a):] = [val] * (length - len(a))

    @staticmethod
    def add(l: list, r) -> list:
        if type(r) is int:
            res = l[:]
            res[0] = (res[0] + r) % MOD
            return res
        if type(r) is list:
            if len(l) < len(r):
                res = r[::]
                for i, x in enumerate(l): res[i] += x
            else:
                res = l[::]
                for i, x in enumerate(r): res[i] += x
            return [x % MOD for x in res]
        raise TypeError()

    @classmethod
    def sub(cls, l: list, r) -> list:
        if type(r) is int: return cls.add(l, -r)
        if type(r) is list: return cls.add(l, cls.neg(r))
        raise TypeError()

    @staticmethod
    def neg(a: list) -> list:
        return [MOD - x if x else 0 for x in a]

    @staticmethod
    def mul(l: list, r) -> list:
        if type(r) is int: return [x * r % MOD for x in l]
        if type(r) is list: return NTT.multiply(l, r)
        raise TypeError()

    @staticmethod
    def matmul(l: list, r: list) -> list:
        'not verified'
        return [x * r[i] % MOD for i, x in enumerate(l)]

    @classmethod
    def div(cls, l: list, r: list) -> list:
        if len(l) < len(r): return []
        n = len(l) - len(r) + 1
        cnt = 0
        if len(r) > 64:
            return NTT.multiply(l[::-1][:n], cls.inv(r[::-1], n))[:n][::-1]
        f, g = l[::], r[::]
        while g and not g[-1]:
            g.pop()
            cnt += 1
        coef = pow(g[-1], MOD - 2, MOD)
        g = cls.mul(g, coef)
        deg = len(f) - len(g) + 1
        gs = len(g)
        quo = [0] * deg
        for i in range(deg)[::-1]:
            quo[i] = x = f[i + gs - 1] % MOD
            for j, y in enumerate(g):
                f[i + j] -= x * y
        return cls.mul(quo, coef) + [0] * cnt

    @classmethod
    def mod(cls, l: list, r: list) -> list:
        res = cls.sub(l, NTT.multiply(cls.div(l, r),  r))
        cls.shrink(res)
        return res

    @classmethod
    def divmod(cls, l: list, r: list):
        quo = cls.div(l, r)
        rem = cls.sub(l, NTT.multiply(quo, r))
        cls.shrink(rem)
        return quo, rem

    @staticmethod
    def eval(a: list, x: int) -> int:
        r = 0; w = 1
        for v in a:
            r += w * v % MOD
            w = w * x % MOD
        return r % MOD

    @staticmethod
    def inv(a: list, deg: int=-1) -> list:
        # assert(self[0] != 0)
        if deg == -1: deg = len(a)
        res = [0] * deg
        res[0] = pow(a[0], MOD - 2, MOD)
        d = 1
        while d < deg:
            f = [0] * (d << 1)
            tmp = min(len(a), d << 1)
            f[:tmp] = a[:tmp]
            g = [0] * (d << 1)
            g[:d] = res[:d]
            NTT.ntt(f)
            NTT.ntt(g)
            for i, x in enumerate(g): f[i] = f[i] * x % MOD
            NTT.intt(f)
            f[:d] = [0] * d
            NTT.ntt(f)
            for i, x in enumerate(g): f[i] = f[i] * x % MOD
            NTT.intt(f)
            for j in range(d, min(d << 1, deg)):
                if f[j]: res[j] = MOD - f[j]
                else: res[j] = 0
            d <<= 1
        return res

    @classmethod
    def pow(cls, a: list, k: int, deg=-1) -> list:
        n = len(a)
        if deg == -1: deg = n
        if k == 0:
            if not deg: return []
            ret = [0] * deg
            ret[0] = 1
            return ret
        for i, x in enumerate(a):
            if x:
                rev = pow(x, MOD - 2, MOD)
                ret = cls.mul(cls.exp(cls.mul(cls.log(cls.mul(a, rev)[i:], deg),  k), deg), pow(x, k, MOD))
                ret[:0] = [0] * (i * k)
                if len(ret) < deg:
                    cls.resize(ret, deg)
                    return ret
                return ret[:deg]
            if (i + 1) * k >= deg: break
        return [0] * deg

    @staticmethod
    def exp(a: list, deg=-1) -> list:
        # assert(not self or self[0] == 0)
        if deg == -1: deg = len(a)
        inv = [0, 1]

        def inplace_integral(F: list) -> list:
            n = len(F)
            while len(inv) <= n:
                j, k = divmod(MOD, len(inv))
                inv.append((-inv[k] * j) % MOD)
            return [0] + [x * inv[i + 1] % MOD for i, x in enumerate(F)]

        def inplace_diff(F: list) -> list:
            return [x * i % MOD for i, x in enumerate(F) if i]

        b = [1, (a[1] if 1 < len(a) else 0)]
        c = [1]
        z1 = []
        z2 = [1, 1]
        m = 2
        while m < deg:
            y = b + [0] * m
            NTT.ntt(y)
            z1 = z2
            z = [y[i] * p % MOD for i, p in enumerate(z1)]
            NTT.intt(z)
            z[:m >> 1] = [0] * (m >> 1)
            NTT.ntt(z)
            for i, p in enumerate(z1): z[i] = z[i] * (-p) % MOD
            NTT.intt(z)
            c[m >> 1:] = z[m >> 1:]
            z2 = c + [0] * m
            NTT.ntt(z2)
            tmp = min(len(a), m)
            x = a[:tmp] + [0] * (m - tmp)
            x = inplace_diff(x)
            x.append(0)
            NTT.ntt(x)
            for i, p in enumerate(x): x[i] = y[i] * p % MOD
            NTT.intt(x)
            for i, p in enumerate(b):
                if not i: continue
                x[i - 1] -= p * i % MOD
            x += [0] * m
            for i in range(m - 1): x[m + i], x[i] = x[i], 0
            NTT.ntt(x)
            for i, p in enumerate(z2): x[i] = x[i] * p % MOD
            NTT.intt(x)
            x.pop()
            x = inplace_integral(x)
            x[:m] = [0] * m
            for i in range(m, min(len(a), m << 1)): x[i] += a[i]
            NTT.ntt(x)
            for i, p in enumerate(y): x[i] = x[i] * p % MOD
            NTT.intt(x)
            b[m:] = x[m:]
            m <<= 1
        return b[:deg]

    @classmethod
    def log(cls, a: list, deg=-1) -> list:
        # assert(a[0] == 1)
        if deg == -1: deg = len(a)
        return cls.integral(cls.mul(cls.diff(a), cls.inv(a, deg))[:deg - 1])

    @staticmethod
    def integral(a: list) -> list:
        n = len(a)
        res = [0] * (n + 1)
        if n: res[1] = 1
        for i in range(2, n + 1):
            j, k = divmod(MOD, i)
            res[i] = (-res[k] * j) % MOD
        for i, x in enumerate(a): res[i + 1] = res[i + 1] * x % MOD
        return res

    @staticmethod
    def diff(a: list) -> list:
        return [i * x % MOD for i, x in enumerate(a) if i]
