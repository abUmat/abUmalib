# my module
from fps.lagrange_interpolation_point import *
# my module
def exp_enumerate(p: int, n: int, mod: int) -> list:
    f = [0] * (n + 1)
    if not p:
        f[0] = 1
        return f
    f[1] = 1
    sieve = [0] * (n + 1)
    ps = []
    for i in range(2, n + 1):
        if not sieve[i]:
            f[i] = pow(i, p, mod)
            ps.append(i)
        for j in range(len(ps)):
            if i * ps[j] > n: break
            sieve[i * ps[j]] = 1
            f[i * ps[j]] = f[i] * f[ps[j]] % mod
            if i % ps[j] == 0: break
    return f

def sum_of_exp(f: list, a: int, n: int, C: Binomial, mod: int) -> int:
    'destructive'
    if n == 0: return 0
    if a == 0: return f[0]
    if a == 1:
        g = [0] * (len(f) + 1)
        tmp = 0
        for i, x in enumerate(f): g[i + 1] = tmp = tmp + x
        return lagrange_interpolation(g, n, C, mod)

    m = len(f)
    buf = 1
    for i in range(m):
        f[i] = f[i] * buf % mod
        buf = buf * a % mod
    for i in range(m - 1): f[i + 1] = (f[i + 1] + f[i]) % mod

    c = 0
    buf = 1
    b = mod - a
    for i in range(m):
        c += (C.C(m, i) * buf % mod) * f[-i - 1] % mod
        buf = buf * b % mod
    c = (c % mod) * pow(pow(mod - a + 1, m, mod), mod - 2, mod) % mod

    buf = 1
    ia = pow(a, mod - 2, mod)
    for i in range(m):
        f[i] = (f[i] - c) * buf % mod
        buf = buf * ia % mod
    tn = lagrange_interpolation(f, n - 1, C, mod)
    return (tn * pow(a, n - 1, mod) + c) % mod

def sum_of_exp2(d: int, r: int, n: int, C: Binomial, mod: int) -> int:
    f = exp_enumerate(d, d, mod)
    return sum_of_exp(f, r, n, C, mod)

def sum_of_exp_limit(f: list, a: int, C: Binomial, mod: int) -> int:
    'destructive'
    if a == 0: return f[0]
    m = len(f)
    buf = 1
    for i in range(m):
        f[i] = f[i] * buf % mod
        buf = buf * a % mod
    for i in range(m - 1): f[i + 1] = (f[i + 1] + f[i]) % mod
    c = 0
    buf = 1
    b = mod - a
    for i in range(m):
        c += (C.C(m, i) * buf % mod) * f[-i - 1] % mod
        buf = buf * b % mod
    c = (c % mod) * pow(pow((-a + 1) % mod, m, mod), mod - 2, mod) % mod
    return c

def sum_of_exp_limit2(d: int, r: int, C: Binomial, mod: int) -> int:
    f = exp_enumerate(d, d, mod)
    return sum_of_exp_limit(f, r, C, mod)
