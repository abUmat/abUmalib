from collections import defaultdict
# my module
from prime.fast_factorize import *
# my module
class _Memo:
    def __init__(self, g: int, s: int, period: int, mod: int):
        self.lg = min(s, period).bit_length() - 1
        self.size = size = 1 << self.lg
        self.mask = mask = size - 1
        self.period = period
        self.mod = mod
        self.vs = vs = [[0, 0] for _ in range(size)]
        self.os = os = [0] * (size + 1)
        x = 1
        for i in range(size):
            os[x & mask] += 1
            x = x * g % mod
        for i in range(1, size): os[i] += os[i - 1]
        x = 1
        for i in range(size):
            tmp = os[x & mask] - 1
            vs[tmp] = [x, i]
            os[x & mask] = tmp
            x = x * g  % mod
        self.gpow = x
        os[size] = size

    def find(self, x: int) -> int:
        size = self.size; period = self.period; mod = self.mod; gpow = self.gpow; mask = self.mask
        os = self.os; vs = self.vs
        t = 0
        while t < period:
            m = x & mask
            i = os[m]
            while i < os[m + 1]:
                if x == vs[i][0]:
                    res = vs[i][1] - t
                    return res + period if res < 0 else res
                i += 1
            t += size
            x = x * gpow % mod

def _pe_root(c: int, pi: int, ei: int, p: int) -> int:
    s = p - 1; t = 0
    while not s % pi:
        s //= pi
        t += 1
    pe = pow(pi, ei)

    u = _inv(pe - s % pe, pe)
    mc = c % p
    z = pow(mc, (s * u + 1) // pe, p)
    zpe = pow(mc, s * u, p)
    if zpe == 1: return z

    ptm1 = pow(pi, t - 1)
    v = 2
    vs = pow(v, s, p)
    v = 3
    while pow(vs, ptm1, p) == 1:
        vs = pow(v, s, p)
        v += 1
    vspe = pow(vs, pe, p)
    vs_e = ei
    base = vspe
    for _ in range(t - ei - 1): base = pow(base, pi, p)
    memo = _Memo(base, int((t - ei) ** 0.5 * pi ** 0.5) + 1, pi, p)

    while zpe != 1:
        tmp = zpe
        td = 0
        while tmp != 1:
            td += 1
            tmp = pow(tmp, pi, p)
        e = t - td
        while vs_e != e:
            vs = pow(vs, pi, p)
            vspe = pow(vspe, pi, p)
            vs_e += 1

        base_zpe = pow(zpe, p - 2, p)
        for _ in range(td - 1): base_zpe = pow(base_zpe, pi, p)
        bsgs = memo.find(base_zpe)
        z = z * pow(vs, bsgs, p) % p
        zpe = zpe * pow(vspe, bsgs, p) % p
    return z

def _kth_root(a: int, k: int, p: int) -> int:
    a %= p
    if k == 0: return a if a == 1 else -1
    if a <= 1 or k <= 1: return a
    g = gcd2(p - 1, k)
    if pow(a, (p - 1) // g, p) != 1: return -1
    a = pow(a, _inv(k // g, (p - 1) // g), p)
    fac = defaultdict(int)
    for prime, cnt in factorize(g).items(): fac[prime] += cnt
    for k, v in fac.items(): a = _pe_root(a, k, v, p)
    return a

def kth_root(a: int, k: int, p: int) -> int:
    """
    X s.t. pow(X, k) == a (mod p)
    """
    return _kth_root(a, k, p)

def _inv(a: int, p: int) -> int:
    b = p; x = 1; y = 0
    while a:
        q = b // a
        a, b = b % a, a
        x, y = y - q * x, x
    return y + p if y < 0 else y
