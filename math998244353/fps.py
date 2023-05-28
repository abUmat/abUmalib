# my module
from math998244353.ntt import *
# my module
# https://nyaannyaan.github.io/library/fps/formal-power-series.hpp
# https://nyaannyaan.github.io/library/fps/ntt-friendly-fps.hpp
class FPS:
    @staticmethod
    def shrink(a: Poly) -> None:
        '''remove high degree coef == 0'''
        while a and not a[-1]: a.pop()

    @staticmethod
    def resize(a: Poly, length: int, val: int=0) -> None:
        a[length:] = []
        a[len(a):] = [val] * (length - len(a))

    @staticmethod
    def add(l: Poly, r: Union[Poly, int]) -> Poly:
        '''l += r'''
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
    def sub(cls, l: Poly, r: Union[Poly, int]) -> Poly:
        '''l -= r'''
        if type(r) is int: return cls.add(l, -r)
        if type(r) is list: return cls.add(l, cls.neg(r))
        raise TypeError()

    @staticmethod
    def neg(a: Poly) -> Poly:
        '''a *= -1'''
        return [MOD - x if x else 0 for x in a]

    @staticmethod
    def mul(l: Poly, r: Union[Poly, int]) -> Poly:
        '''
        if r is int: l *= r
        if r is Polynomial: convolve l and r
        '''
        if type(r) is int: return [x * r % MOD for x in l]
        if type(r) is list:
            if not l or not r: return []
            return NTT.multiply(l, r)
        raise TypeError()

    @staticmethod
    def matmul(l: Poly, r: Poly) -> Poly:
        'not verified'
        return [x * r[i] % MOD for i, x in enumerate(l)]

    @classmethod
    def div(cls, l: Poly, r: Poly) -> Poly:
        '''return: quo s.t. l = r*quo + rem'''
        if len(l) < len(r): return []
        n = len(l) - len(r) + 1
        if len(r) > 64:
            return NTT.multiply(l[::-1][:n], cls.inv(r[::-1], n))[:n][::-1]
        f, g = l[::], r[::]
        cnt = 0
        while g and not g[-1]:
            g.pop()
            cnt += 1
        coef = modinv(g[-1], MOD)
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
    def modulo(cls, l: Poly, r: Poly) -> Poly:
        '''return: rem s.t. l = r*quo + rem'''
        res = cls.sub(l, NTT.multiply(cls.div(l, r), r))
        cls.shrink(res)
        return res

    @classmethod
    def divmod(cls, l: Poly, r: Poly) -> Tuple[Poly, Poly]:
        '''return: quo, rem s.t. l = r*quo + rem'''
        quo = cls.div(l, r)
        rem = cls.sub(l, NTT.multiply(quo, r))
        cls.shrink(rem)
        return quo, rem

    @staticmethod
    def eval(a: Poly, x: int) -> int:
        r = 0; w = 1
        for v in a:
            r += w * v % MOD
            w = w * x % MOD
        return r % MOD

    @staticmethod
    def inv(a: Poly, deg: int=-1) -> Poly:
        '''return: g s.t. a*g == 1 (mod x**deg)'''
        # assert(self[0] != 0)
        if deg == -1: deg = len(a)
        res = [0] * deg
        res[0] = modinv(a[0], MOD)
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
    def pow(cls, f: Poly, k: int, deg=-1) -> Poly:
        '''return: g s.t. g == f**k (mod x**deg)'''
        n = len(f)
        if deg == -1: deg = n
        if k == 0:
            if not deg: return []
            ret = [0] * deg
            ret[0] = 1
            return ret
        for i, x in enumerate(f):
            if x:
                rev = modinv(x, MOD)
                ret = cls.mul(cls.exp(cls.mul(cls.log(cls.mul(f, rev)[i:], deg),  k), deg), pow(x, k, MOD))
                ret[:0] = [0] * (i * k)
                if len(ret) < deg:
                    cls.resize(ret, deg)
                    return ret
                return ret[:deg]
            if (i + 1) * k >= deg: break
        return [0] * deg

    @staticmethod
    def exp(f: Poly, deg: int=-1) -> Poly:
        '''return: g s.t. log(g) == f (mod x ** deg)'''
        # assert(not self or self[0] == 0)
        if deg == -1: deg = len(f)
        inv = [0, 1]

        def integral(f: Poly) -> Poly:
            n = len(f)
            while len(inv) <= n:
                j, k = divmod(MOD, len(inv))
                inv.append((-inv[k] * j) % MOD)
            return [0] + [x * inv[i + 1] % MOD for i, x in enumerate(f)]

        def diff(f: Poly) -> Poly:
            return [x * i % MOD for i, x in enumerate(f) if i]

        b: Poly = [1, (f[1] if 1 < len(f) else 0)]
        c: Poly = [1]
        z1: Poly= []
        z2: Poly = [1, 1]
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
            tmp = min(len(f), m)
            x = f[:tmp] + [0] * (m - tmp)
            x = diff(x)
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
            x = integral(x)
            x[:m] = [0] * m
            for i in range(m, min(len(f), m << 1)): x[i] += f[i]
            NTT.ntt(x)
            for i, p in enumerate(y): x[i] = x[i] * p % MOD
            NTT.intt(x)
            b[m:] = x[m:]
            m <<= 1
        return b[:deg]

    @classmethod
    def log(cls, f: Poly, deg=-1) -> Poly:
        '''return: g s.t. g == log(f) (mod x**deg)'''
        # assert(a[0] == 1)
        if deg == -1: deg = len(f)
        return cls.integral(cls.mul(cls.diff(f), cls.inv(f, deg))[:deg - 1])

    @staticmethod
    def integral(f: Poly) -> Poly:
        n = len(f)
        res = [0] * (n + 1)
        if n: res[1] = 1
        for i in range(2, n + 1):
            j, k = divmod(MOD, i)
            res[i] = (-res[k] * j) % MOD
        for i, x in enumerate(f): res[i + 1] = res[i + 1] * x % MOD
        return res

    @staticmethod
    def diff(f: Poly) -> Poly:
        '''return: dfdx'''
        return [i * x % MOD for i, x in enumerate(f) if i]
