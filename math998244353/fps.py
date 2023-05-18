from math import log2
# my module
from math998244353.ntt import *
from modulo.mod_sqrt import *
# my module
# https://nyaannyaan.github.io/library/fps/formal-power-series.hpp
def fps_add(a: list, b: list) -> list:
    if len(a) < len(b):
        res = b[::]
        for i, x in enumerate(a): res[i] += x
    else:
        res = a[::]
        for i, x in enumerate(b): res[i] += x
    return [x % MOD for x in res]

def fps_add_scalar(a: list, k: int) -> list:
    res = a[:]
    res[0] = (res[0] + k) % MOD
    return res

def fps_sub(a: list, b: list) -> list:
    if len(a) < len(b):
        res = b[::]
        for i, x in enumerate(a): res[i] -= x
        res = fps_neg(res)
    else:
        res = a[::]
        for i, x in enumerate(b): res[i] -= x
    return [x % MOD for x in res]

def fps_sub_scalar(a: list, k: int) -> list:
    return fps_add_scalar(a, -k)

def fps_neg(a: list) -> list:
    return [MOD - x if x else 0 for x in a]

def fps_mul_scalar(a: list, k: int) -> list:
    return [x * k % MOD for x in a]

def fps_matmul(a: list, b: list) -> list:
    'not verified'
    return [x * b[i] % MOD for i, x in enumerate(a)]

def fps_div(a: list, b: list) -> list:
    if len(a) < len(b): return []
    n = len(a) - len(b) + 1
    cnt = 0
    if len(b) > 64:
        return multiply(a[::-1][:n], fps_inv(b[::-1], n))[:n][::-1]
    f, g = a[::], b[::]
    while g and not g[-1]:
        g.pop()
        cnt += 1
    coef = pow(g[-1], MOD - 2, MOD)
    g = fps_mul_scalar(g, coef)
    deg = len(f) - len(g) + 1
    gs = len(g)
    quo = [0] * deg
    for i in range(deg)[::-1]:
        quo[i] = x = f[i + gs - 1] % MOD
        for j, y in enumerate(g):
            f[i + j] -= x * y
    return fps_mul_scalar(quo, coef) + [0] * cnt

def fps_mod(a: list, b: list) -> list:
    res = fps_sub(a, multiply(fps_div(a, b),  b))
    while res and not res[-1]: res.pop()
    return res

def fps_divmod(a: list, b: list):
    q = fps_div(a, b)
    r = fps_sub(a, multiply(q, b))
    while r and not r[-1]: r.pop()
    return q, r

def fps_eval(a: list, x: int) -> int:
    r = 0; w = 1
    for v in a:
        r += w * v % MOD
        w = w * x % MOD
    return r % MOD

def fps_inv(a: list, deg: int=-1) -> list:
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

def fps_pow(a: list, k: int, deg=-1) -> list:
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
            ret = fps_mul_scalar(fps_exp(fps_mul_scalar(fps_log(fps_mul_scalar(a, rev)[i:], deg),  k), deg), pow(x, k, MOD))
            ret[:0] = [0] * (i * k)
            if len(ret) < deg:
                ret[len(ret):] = [0] * (deg - len(ret))
                return ret
            return ret[:deg]
        if (i + 1) * k >= deg: break
    return [0] * deg

def fps_exp(a: list, deg=-1) -> list:
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

def fps_log(a: list, deg=-1) -> list:
    # assert(a[0] == 1)
    if deg == -1: deg = len(a)
    return fps_integral(multiply(fps_diff(a), fps_inv(a, deg))[:deg - 1])

def fps_integral(a: list) -> list:
    n = len(a)
    res = [0] * (n + 1)
    if n: res[1] = 1
    for i in range(2, n + 1):
        j, k = divmod(MOD, i)
        res[i] = (-res[k] * j) % MOD
    for i, x in enumerate(a): res[i + 1] = res[i + 1] * x % MOD
    return res

def fps_diff(a: list) -> list:
    return [i * x % MOD for i, x in enumerate(a) if i]
