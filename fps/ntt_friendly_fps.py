# my module
from ntt.ntt import *
from fps.formal_power_series import *
# my module
def set_fft(self : FormalPowerSeries):
    if not self.ntt_ptr: self.ntt_ptr = NTT(self.mod)
FormalPowerSeries.set_fft = set_fft

def __mul__(self: FormalPowerSeries, r) -> FormalPowerSeries:
    if type(r) is int:
        res = FormalPowerSeries([x * r for x in self])
        res.mod = self.mod
        res.reduction()
        return res
    if not self and not r:
        res = FormalPowerSeries()
        res.mod = self.mod
        return res
    self.set_fft()
    res = self.ntt_ptr.multiply(self, r)
    res = FormalPowerSeries(res)
    res.mod = self.mod
    return res
FormalPowerSeries.__mul__ = __mul__

def ntt(self: FormalPowerSeries) -> None:
    self.set_fft()
    self.ntt_ptr.ntt(self)
FormalPowerSeries.ntt = ntt

def intt(self: FormalPowerSeries) -> None:
    self.set_fft()
    self.ntt_ptr.intt(self)
FormalPowerSeries.intt = intt

def ntt_doubling(self: FormalPowerSeries) -> None:
    self.set_fft()
    self.ntt_ptr.ntt_doubling(self)
FormalPowerSeries.ntt_doubling = ntt_doubling

def ntt_pr(self: FormalPowerSeries) -> int:
    self.set_fft()
    return self.ntt_ptr.pr
FormalPowerSeries.ntt_pr = ntt_pr

def inv(self: FormalPowerSeries, deg=-1) -> FormalPowerSeries:
    # assert(self[0] != 0)
    mod = self.mod
    ntt = NTT(mod)
    if deg == -1: deg = len(self)
    res = FormalPowerSeries([0] * deg)
    res.mod = mod
    res[0] = pow(self[0], mod - 2, mod)
    d = 1
    while d < deg:
        f = [0] * (d << 1)
        g = [0] * (d << 1)
        tmp = min(len(self), d << 1)
        f[:tmp] = self[:tmp]
        g[:d] = res[:d]
        ntt.ntt(f)
        ntt.ntt(g)
        f = [x * y % mod for x, y in zip(f, g)]
        ntt.intt(f)
        f[:d] = [0] * d
        ntt.ntt(f)
        f = [x * y % mod for x, y in zip(f, g)]
        ntt.intt(f)
        for j in range(d, min(d << 1, deg)):
            if f[j]: res[j] = mod - f[j]
            else: res[j] = 0
        d <<= 1
    return res[:deg]
FormalPowerSeries.inv = inv

def exp(self: FormalPowerSeries, deg=-1) -> FormalPowerSeries:
    # assert(not self or self[0] == 0)
    if deg == -1: deg = len(self)
    mod = self.mod
    ntt = NTT(mod)
    inv = [0, 1]

    def inplace_integral(F: List[int]) -> List[int]:
        n = len(F)
        while len(inv) <= n:
            j, k = divmod(mod, len(inv))
            inv.append((-inv[k] * j) % mod)
        return [0] + [x * inv[i + 1] % mod for i, x in enumerate(F)]

    def inplace_diff(F: List[int]) -> List[int]:
        return [x * i % mod for i, x in enumerate(F) if i]

    b = [1, (self[1] if 1 < len(self) else 0)]
    c = [1]
    z1 = []
    z2 = [1, 1]
    m = 2
    while m < deg:
        y = b + [0] * m
        ntt.ntt(y)
        z1 = z2
        z = [p * q for p, q in zip(y, z1)]
        ntt.intt(z)
        z[:m >> 1] = [0] * (m >> 1)
        ntt.ntt(z)
        z = [-(p * q) % mod for p, q in zip(z, z1)]
        ntt.intt(z)
        c[m >> 1:] = z[m >> 1:]
        z2 = c + [0] * m
        ntt.ntt(z2)
        tmp = min(len(self), m)
        x = self[:tmp] + [0] * (m - tmp)
        x = inplace_diff(x)
        x.append(0)
        ntt.ntt(x)
        x = [p * q % mod for p, q in zip(x, y)]
        ntt.intt(x)
        for i in range(len(b) - 1): x[i] -= b[i + 1] * (i + 1) % mod
        x += [0] * m
        for i in range(m - 1): x[m + i], x[i] = x[i], 0
        ntt.ntt(x)
        x = [p * q % mod for p, q in zip(x, z2)]
        ntt.intt(x)
        x.pop()
        x = inplace_integral(x)
        for i in range(min(len(self), m << 1)):
            if i < m: x[i] = 0
            else:
                x[i] += self[i]
                if x[i] >= mod: x[i] -= mod
        ntt.ntt(x)
        x = [p * q % mod for p, q in zip(x, y)]
        ntt.intt(x)
        b[m:] = x[m:]
        m <<= 1
    return b[:deg]
FormalPowerSeries.exp = exp

