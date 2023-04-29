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
    inv = FormalPowerSeries([0, 1]); inv.mod = mod

    def inplace_integral(F: FormalPowerSeries) -> FormalPowerSeries:
        n = len(F)
        while len(inv) <= n:
            i = len(inv)
            j, k = divmod(mod, i)
            inv.append(-inv[k] * j % mod)
        F = FormalPowerSeries([x * inv[i + 1] % mod for i, x in enumerate(F)]); F.mod = mod
        F.insert(0, 0)
        return F

    def inplace_diff(F: FormalPowerSeries) -> FormalPowerSeries:
        if not F: return
        F = F[1:]
        coef = 1
        F = FormalPowerSeries([x * (i + 1) % mod for i, x in enumerate(F)]); F.mod = mod
        return F

    b = FormalPowerSeries([1, (self[1] if 1 < len(self) else 0)]); b.mod = mod
    c = FormalPowerSeries([1]); c.mod = mod
    z1 = FormalPowerSeries(); z1.mod = mod
    z2 = FormalPowerSeries([1, 1]); z2.mod = mod
    m = 2
    while m < deg:
        y = b.resized(m << 1)
        y.ntt()
        z1 = z2
        z = FormalPowerSeries([y[i] * z1[i] % mod for i in range(m)]); z.mod = mod
        z.intt()
        z[:m >> 1] = [0] * (m >> 1)
        z.ntt()
        for i in range(m): z[i] = z[i] * -z1[i] % mod
        z.intt()
        c[m >> 1:] = z[m >> 1:]
        z2 = c.resized(m << 1)
        z2.ntt()
        x = FormalPowerSeries(self[:min(len(self), m)]); x.mod = mod
        x = x.resized(m)
        x = inplace_diff(x)
        x.append(0)
        x.ntt()
        for i in range(m): x[i] = x[i] * y[i] % mod
        x.intt()
        x -= b.diff()
        x = x.resized(m << 1)
        for i in range(m - 1): x[m + i], x[i] = x[i], 0
        x.ntt()
        for i in range(m << 1): x[i] = x[i] * z2[i] % mod
        x.intt()
        x.pop()
        x = inplace_integral(x)
        for i in range(min(len(self), m << 1)):
            if i < m: x[i] = 0
            else:
                x[i] += self[i]
                if x[i] >= mod: x[i] -= mod
        x.ntt()
        for i in range(m << 1): x[i] = x[i] * y[i] % mod
        x.intt()
        b[m:] = x[m:]
        m <<= 1
    return b[:deg]
FormalPowerSeries.exp = exp

