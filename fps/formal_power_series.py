class FormalPowerSeries(list):
    mod = 0
    ntt_ptr = None

    def reduction(self, mod=0):
        if not mod: mod = self.mod
        for i in range(len(self)): self[i] %= mod

    def __add__(self, r):
        if type(r) is int:
            if self: res = FormalPowerSeries([x if i else x + r for i, x in enumerate(self)])
            else: res = FormalPowerSeries([r])
        elif len(self) < len(r):
            res = r[::]
            for i, x in enumerate(self): res[i] += x
        else:
            res = self[::]
            for i, x in enumerate(r): res[i] += x
        res.mod = self.mod
        return res

    def __sub__(self, r):
        if type(r) is int:
            if self: res = FormalPowerSeries([x if i else x - r for i, x in enumerate(self)])
            else: res = FormalPowerSeries([r])
        elif len(self) < len(r):
            res = r[::]
            for i, x in enumerate(self): res[i] -= x
            res = -res
        else:
            res = self[::]
            for i, x in enumerate(r): res[i] -= x
        res.mod = self.mod
        return res

    def __mul__(self, r):
        mod = self.mod
        res = FormalPowerSeries([x * r % mod for x in self]); res.mod = mod
        return res

    def __matmul__(self, r):
        mod = self.mod
        n = min(len(self), len(r))
        res = FormalPowerSeries([self[i] * r[i] % mod for i in range(n)]); res.mod = mod
        return res

    def __truediv__(self, r):
        mod = self.mod
        if len(self) < len(r):
            res = FormalPowerSeries(); res.mod = mod
            return res
        n = len(self) - len(r) + 1
        if len(r) <= 64:
            f, g = self[::], r[::]
            g.shrink()
            coef = pow(g[-1], mod-2, mod)
            for i in range(len(g)): g[i] *= coef
            deg = len(f) - len(g) + 1
            gs = len(g)
            quo = FormalPowerSeries([0] * deg)
            quo.mod = mod
            for i in range(deg)[::-1]:
                quo[i] = f[i + gs - 1]
                for j in range(gs): f[i + j] -= quo[i] * g[j]
            res = quo * coef
            return res.resized(n)
        return (self[::-1][:n] * r[::-1].inv(n))[:n][::-1]

    def __mod__(self, r):
        res = self - self / r * r
        res.shrink()
        return res

    def __neg__(self):
        mod = self.mod
        res = FormalPowerSeries([mod - x if x else 0 for x in self])
        res.mod = mod
        return res

    def __lshift__(self, sz):
        res = self[::]
        res[:0] = [0] * sz
        return res

    def __getitem__(self, item):
        if type(item) is int: return super().__getitem__(item)
        res = type(self)(super().__getitem__(item))
        res.mod = self.mod
        return res

    def shrink(self):
        while self and not self[-1]: self.pop()

    def resized(self, n):
        res = self[:n]
        if len(res) < n: res[len(res):] = [0] * (n - len(res))
        return res

    def diff(self):
        mod = self.mod
        n = len(self)
        res = FormalPowerSeries([0] * max(0, n - 1)); res.mod = mod
        for i in range(1, n): res[i - 1] = self[i] * i % mod
        return res

    def integral(self):
        mod = self.mod
        n = len(self)
        res = FormalPowerSeries([0] * (n + 1)); res.mod = mod
        if n: res[1] = 1
        for i in range(2, n + 1):
            j, k = divmod(mod, i)
            res[i] = -res[k] * j % mod
        for i in range(n): res[i + 1] = res[i + 1] * self[i] % mod
        return res

    def eval(self, x):
        mod = self.mod
        r = 0; w = 1
        for v in self:
            r += w * v % mod
            w = w * x % mod
        return r

    def log(self, deg=-1):
        # assert(self[0] == 1)
        if deg == -1: deg = len(self)
        return (self.diff() * self.inv(deg))[:deg - 1].integral()

    def pow(self, k, deg=-1):
        mod = self.mod
        n = len(self)
        if deg == -1: deg = n
        if k == 0:
            ret = FormalPowerSeries([0] * deg); ret.mod = mod
            if deg: ret[0] = 1
            return ret
        for i in range(n):
            if self[i] != 0:
                rev = pow(self[i], mod - 2, mod)
                ret = (((self * rev)[i:]).log(deg) * k).exp(deg)
                ret = ret * pow(self[i], k, mod)
                ret = (ret << (i * k))[:deg]
                if len(ret) < deg: return ret.resized(deg)
                return ret
            if (i + 1) * k >= deg: break
        res = FormalPowerSeries([0] * deg); res.mod = mod
        return res
