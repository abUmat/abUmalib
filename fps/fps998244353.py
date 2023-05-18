# my module
from ntt.ntt998244353 import *
from modulo.mod_sqrt import *
from modulo.binomial import *
# my module
def add(a: list, b: list) -> list:
    if len(a) < len(b):
        res = b[::]
        for i, x in enumerate(a): res[i] += x
    else:
        res = a[::]
        for i, x in enumerate(b): res[i] += x
    return [x % MOD for x in res]

def sub(a: list, b: list) -> list:
    if len(a) < len(b):
        res = b[::]
        for i, x in enumerate(a): res[i] -= x
        res = neg(res)
    else:
        res = a[::]
        for i, x in enumerate(b): res[i] -= x
    return [x % MOD for x in res]

def neg(a: list) -> list:
    return [MOD - x if x else 0 for x in a]

def scalar(a: list, k: int) -> list:
    return [x * k % MOD for x in a]

def matmul(a: list, b: list) -> list:
    'not verified'
    return [x * b[i] % MOD for i, x in enumerate(a)]

def div(a: list, b: list) -> list:
    if len(a) < len(b): return []
    n = len(a) - len(b) + 1
    cnt = 0
    if len(b) > 64:
        return multiply(a[::-1][:n], inv(b[::-1], n))[:n][::-1]
    f, g = a[::], b[::]
    while g and not g[-1]:
        g.pop()
        cnt += 1
    coef = pow(g[-1], MOD - 2, MOD)
    g = scalar(g, coef)
    deg = len(f) - len(g) + 1
    gs = len(g)
    quo = [0] * deg
    for i in range(deg)[::-1]:
        quo[i] = x = f[i + gs - 1] % MOD
        for j, y in enumerate(g):
            f[i + j] -= x * y
    return scalar(quo, coef) + [0] * cnt

def modulo(a: list, b: list) -> list:
    res = sub(a, multiply(div(a, b),  b))
    while res and not res[-1]: res.pop()
    return res

def div_mod(a: list, b: list):
    q = div(a, b)
    r = sub(a, multiply(q, b))
    while r and not r[-1]: r.pop()
    return q, r

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
        ntt(f)
        ntt(g)
        for i, x in enumerate(g): f[i] = f[i] * x % MOD
        intt(f)
        f[:d] = [0] * d
        ntt(f)
        for i, x in enumerate(g): f[i] = f[i] * x % MOD
        intt(f)
        for j in range(d, min(d << 1, deg)):
            if f[j]: res[j] = MOD - f[j]
            else: res[j] = 0
        d <<= 1
    return res

def power(a: list, k: int, deg=-1) -> list:
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
            ret = scalar(exp(scalar(log(scalar(a, rev)[i:], deg),  k), deg), pow(x, k, MOD))
            ret[:0] = [0] * (i * k)
            if len(ret) < deg:
                ret[len(ret):] = [0] * (deg - len(ret))
                return ret
            return ret[:deg]
        if (i + 1) * k >= deg: break
    return [0] * deg

def sqrt(a: list, deg=-1) -> list:
    if deg == -1: deg = len(a)
    if len(a) == 0: return [0] * deg
    if a[0] == 0:
        for i in range(1, len(a)):
            if a[i] != 0:
                if i & 1: return []
                if deg - i // 2 <= 0: break
                ret = sqrt(a[i:], deg - i // 2)
                if not ret: return []
                ret[:0] = [0] * (i >> 1)
                if len(ret) < deg: ret[len(ret):] = [0] * (deg - len(ret))
                return ret
        return [0] * deg
    sqr = mod_sqrt(a[0], MOD)
    if sqr == -1: return []
    ret = [sqr]
    inv2 = 499122177
    i = 1
    while i < deg:
        i <<= 1
        ret = scalar(add(ret, multiply(a[:i], inv(ret, i))), inv2)
    return ret[:deg]

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
        ntt(y)
        z1 = z2
        z = [y[i] * p % MOD for i, p in enumerate(z1)]
        intt(z)
        z[:m >> 1] = [0] * (m >> 1)
        ntt(z)
        for i, p in enumerate(z1): z[i] = z[i] * (-p) % MOD
        intt(z)
        c[m >> 1:] = z[m >> 1:]
        z2 = c + [0] * m
        ntt(z2)
        tmp = min(len(a), m)
        x = a[:tmp] + [0] * (m - tmp)
        x = inplace_diff(x)
        x.append(0)
        ntt(x)
        for i, p in enumerate(x): x[i] = y[i] * p % MOD
        intt(x)
        for i, p in enumerate(b):
            if not i: continue
            x[i - 1] -= p * i % MOD
        x += [0] * m
        for i in range(m - 1): x[m + i], x[i] = x[i], 0
        ntt(x)
        for i, p in enumerate(z2): x[i] = x[i] * p % MOD
        intt(x)
        x.pop()
        x = inplace_integral(x)
        x[:m] = [0] * m
        for i in range(m, min(len(a), m << 1)): x[i] += a[i]
        ntt(x)
        for i, p in enumerate(y): x[i] = x[i] * p % MOD
        intt(x)
        b[m:] = x[m:]
        m <<= 1
    return b[:deg]

def log(a: list, deg=-1) -> list:
    # assert(a[0] == 1)
    if deg == -1: deg = len(a)
    return integral(multiply(diff(a), inv(a, deg))[:deg - 1])

def integral(a: list) -> list:
    n = len(a)
    res = [0] * (n + 1)
    if n: res[1] = 1
    for i in range(2, n + 1):
        j, k = divmod(MOD, i)
        res[i] = (-res[k] * j) % MOD
    for i, x in enumerate(a): res[i + 1] = res[i + 1] * x % MOD
    return res

def diff(a: list) -> list:
    return [i * x % MOD for i, x in enumerate(a) if i]

def taylor_shift(f: list, a: int, C: Binomial):
    n = len(f)
    res = [x * C.fac(i) % MOD for i, x in enumerate(f)]
    res.reverse()
    g = [0] * n
    g[0] = tmp = 1
    for i in range(1, n): g[i] = tmp = (tmp * a % MOD) * C.inv(i) % MOD
    res = multiply(res, g)[:n]
    res.reverse()
    return [x * C.finv(i) % MOD for i, x in enumerate(res)]

def stirling1(N: int, C: Binomial) -> list:
    if N <= 0: return [1]
    lg = N.bit_length() - 1
    res = [0, 1]
    for i in range(lg)[::-1]:
        n = N >> i
        res = multiply(res, taylor_shift(res, (n >> 1) % MOD, C))
        if n & 1: res = add([0] + res, scalar(res, n - 1))
    return res

def stirling2(N: int, C: Binomial) -> list:
    f = [pow(i, N, MOD) * C.finv(i) % MOD for i in range(N + 1)]
    g = [-C.finv(i) if i & 1 else C.finv(i) for i in range(N + 1)]
    return multiply(f, g)[:N + 1]

def bernoulli(N: int, C: Binomial) -> list:
    res = [C.finv(i + 1) for i in range(N + 1)]
    res = inv(res, N + 1)
    return [x * C.fac(i) % MOD for i, x in enumerate(res)]

def partition(N: int) -> list:
    res = [0] * (N + 1)
    res[0] = 1
    for k in range(1, N + 1):
        k1 = k * (3 * k + 1) >> 1
        k2 = k * (3 * k - 1) >> 1
        if k2 > N: break
        if k1 <= N: res[k1] += (-1 if k & 1 else 1)
        if k2 <= N: res[k2] += (-1 if k & 1 else 1)
    return inv(res)

def montmort(N: int, mod: int) -> list:
    if N <= 1: return [0]
    if N == 2: return [0, 1]
    f = [0] * N
    f[0] = 0; f[1] = tmp = 1
    for i in range(2, N): f[i] = tmp = (tmp + f[i - 2]) * i % mod
    return f
