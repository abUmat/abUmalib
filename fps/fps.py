# https://nyaannyaan.github.io/library/fps/formal-power-series.hpp
class FPS:
    ntt = None
    def __init__(self, mod: int) -> None:
        self.mod = mod

    @staticmethod
    def shrink(a: list) -> None:
        while a and not a[-1]: a.pop()

    @staticmethod
    def resize(a: list, length: int, val: int=0) -> None:
        a[length:] = []
        a[len(a):] = [val] * (length - len(a))

    def add(self, l: list, r) -> list:
        if type(r) is int:
            res = l[:]
            res[0] = (res[0] + r) % self.mod
            return res
        mod = self.mod
        if type(r) is list:
            if len(l) < len(r):
                res = r[::]
                for i, x in enumerate(l): res[i] += x
            else:
                res = l[::]
                for i, x in enumerate(r): res[i] += x
            return [x % mod for x in res]
        raise TypeError()

    def sub(self, l: list, r) -> list:
        if type(r) is int: return self.add(l, -r)
        if type(r) is list: return self.add(l, self.neg(r))
        raise TypeError()

    def neg(self, a: list) -> list:
        mod = self.mod
        return [mod - x if x else 0 for x in a]

    def matmul(self, l: list, r: list) -> list:
        'not verified'
        mod = self.mod
        return [x * r[i] % mod for i, x in enumerate(l)]

    def div(self, l: list, r: list) -> list:
        if len(l) < len(r): return []
        n = len(l) - len(r) + 1
        if len(r) > 64:
            return self.mul(l[::-1][:n], self.inv(r[::-1], n))[:n][::-1]
        mod = self.mod
        f, g = l[::], r[::]
        cnt = 0
        while g and not g[-1]:
            g.pop()
            cnt += 1
        coef = pow(g[-1], mod - 2, mod)
        g = self.mul(g, coef)
        deg = len(f) - len(g) + 1
        gs = len(g)
        quo = [0] * deg
        for i in range(deg)[::-1]:
            quo[i] = x = f[i + gs - 1] % mod
            for j, y in enumerate(g):
                f[i + j] -= x * y
        return self.mul(quo, coef) + [0] * cnt

    def modulo(self, l: list, r: list) -> list:
        res = self.sub(l, self.mul(self.div(l, r), r))
        self.shrink(res)
        return res

    def divmod(self, l: list, r: list):
        quo = self.div(l, r)
        rem = self.sub(l, self.mul(quo, r))
        self.shrink(rem)
        return quo, rem

    def eval(self, a: list, x: int) -> int:
        mod = self.mod
        r = 0; w = 1
        for v in a:
            r += w * v % mod
            w = w * x % mod
        return r % mod

    def pow(self, a: list, k: int, deg=-1) -> list:
        n = len(a)
        if deg == -1: deg = n
        if k == 0:
            if not deg: return []
            ret = [0] * deg
            ret[0] = 1
            return ret
        mod = self.mod
        for i, x in enumerate(a):
            if x:
                rev = pow(x, mod - 2, mod)
                ret = self.mul(self.exp(self.mul(self.log(self.mul(a, rev)[i:], deg), k), deg), pow(x, k, mod))
                ret[:0] = [0] * (i * k)
                if len(ret) < deg:
                    self.resize(ret, deg)
                    return ret
                return ret[:deg]
            if (i + 1) * k >= deg: break
        return [0] * deg

    def log(self, a: list, deg=-1) -> list:
        # assert(a[0] == 1)
        if deg == -1: deg = len(a)
        return self.integral(self.mul(self.diff(a), self.inv(a, deg))[:deg - 1])

    def integral(self, a: list) -> list:
        mod = self.mod
        n = len(a)
        res = [0] * (n + 1)
        if n: res[1] = 1
        for i in range(2, n + 1):
            j, k = divmod(mod, i)
            res[i] = (-res[k] * j) % mod
        for i, x in enumerate(a): res[i + 1] = res[i + 1] * x % mod
        return res

    def diff(self, a: list) -> list:
        mod = self.mod
        return [i * x % mod for i, x in enumerate(a) if i]

    def mul(self, l: list, r) -> list:
        raise AttributeError("type object 'FPS' has no attribute 'mul'")

    def mul2(self, l: list) -> list:
        raise AttributeError("type object 'FPS' has no attribute 'mul2'")

    def inv(self, a: list, deg: int=-1) -> list:
        raise AttributeError("type object 'FPS' has no attribute 'inv'")

    def exp(self, a: list, deg: int=-1) -> list:
        raise AttributeError("type object 'FPS' has no attribute 'exp'")
