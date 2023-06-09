# my module
from ntt.ntt import *
from fps.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/ntt-friendly-fps.hpp
def __init__(self, mod: int) -> None:
    self.mod = mod
    self.ntt = NTT(mod)
FPS.__init__ = __init__

def mul(self: FPS, l: Poly, r: Union[Poly, int]) -> Poly:
    '''
    if r is int: l *= r
    if r is Polynomial: convolve l and r
    '''
    mod = self.mod
    if type(r) is int: return [x * r % mod for x in l]
    if type(r) is list:
        if not l or not r: return []
        return self.ntt.multiply(l, r)
    raise TypeError()
FPS.mul = mul

def inv(self: FPS, a: Poly, deg: int=-1) -> Poly:
    '''return: g s.t. a*g == 1 (mod x**deg)'''
    # assert(self[0] != 0)
    mod = self.mod
    if deg == -1: deg = len(a)
    res = [0] * deg
    res[0] = pow(a[0], mod - 2, mod)
    d = 1
    while d < deg:
        f = [0] * (d << 1)
        g = [0] * (d << 1)
        tmp = min(len(a), d << 1)
        f[:tmp] = a[:tmp]
        g[:d] = res[:d]
        self.ntt.ntt(f)
        self.ntt.ntt(g)
        for i, x in enumerate(g): f[i] = f[i] * x % mod
        self.ntt.intt(f)
        f[:d] = [0] * d
        self.ntt.ntt(f)
        for i, x in enumerate(g): f[i] = f[i] * x % mod
        self.ntt.intt(f)
        for j in range(d, min(d << 1, deg)):
            if f[j]: res[j] = mod - f[j]
            else: res[j] = 0
        d <<= 1
    return res
FPS.inv = inv

def exp(self: FPS, f: Poly, deg: int=-1) -> Poly:
    '''return: g s.t. log(g) == f (mod x ** deg)'''
    # assert(not self or self[0] == 0)
    mod = self.mod
    if deg == -1: deg = len(f)
    inv = [0, 1]

    def integral(f: list) -> list:
        n = len(f)
        while len(inv) <= n:
            j, k = divmod(mod, len(inv))
            inv.append((-inv[k] * j) % mod)
        return [0] + [x * inv[i + 1] % mod for i, x in enumerate(f)]

    def diff(f: list) -> list:
        return [x * i % mod for i, x in enumerate(f) if i]

    b = [1, (f[1] if 1 < len(f) else 0)]
    c = [1]
    z1 = []
    z2 = [1, 1]
    m = 2
    while m < deg:
        y = b + [0] * m
        self.ntt.ntt(y)
        z1 = z2
        z = [y[i] * p % mod for i, p in enumerate(z1)]
        self.ntt.intt(z)
        z[:m >> 1] = [0] * (m >> 1)
        self.ntt.ntt(z)
        for i, p in enumerate(z1): z[i] = z[i] * (-p) % mod
        self.ntt.intt(z)
        c[m >> 1:] = z[m >> 1:]
        z2 = c + [0] * m
        self.ntt.ntt(z2)
        tmp = min(len(f), m)
        x = f[:tmp] + [0] * (m - tmp)
        x = diff(x)
        x.append(0)
        self.ntt.ntt(x)
        for i, p in enumerate(x): x[i] = y[i] * p % mod
        self.ntt.intt(x)
        for i, p in enumerate(b):
            if not i: continue
            x[i - 1] -= p * i % mod
        x += [0] * m
        for i in range(m - 1): x[m + i], x[i] = x[i], 0
        self.ntt.ntt(x)
        for i, p in enumerate(z2): x[i] = x[i] * p % mod
        self.ntt.intt(x)
        x.pop()
        x = integral(x)
        x[:m] = [0] * m
        for i in range(m, min(len(f), m << 1)): x[i] += f[i]
        self.ntt.ntt(x)
        for i, p in enumerate(y): x[i] = x[i] * p % mod
        self.ntt.intt(x)
        b[m:] = x[m:]
        m <<= 1
    return b[:deg]
FPS.exp = exp
