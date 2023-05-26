# my module
from fps.taylor_shift import *
# my module
# https://nyaannyaan.github.io/library/fps/fps-famous-series.hpp
def stirling1(N: int, C: Binomial) -> list:
    mod = C.mod
    fps = FPS(mod)
    if N <= 0: return [1]
    lg = N.bit_length() - 1
    res = [0, 1]
    for i in range(lg)[::-1]:
        n = N >> i
        res = fps.mul(res, taylor_shift(res, (n >> 1) % mod, C))
        if n & 1: res = fps.add([0] + res, fps.mul(res, n - 1))
    return res

def stirling2(N: int, C: Binomial) -> list:
    mod = C.mod
    f = [pow(i, N, mod) * C.finv(i) % mod for i in range(N + 1)]
    g = [-C.finv(i) if i & 1 else C.finv(i) for i in range(N + 1)]
    return FPS(mod).mul(f, g)[:N + 1]

def bernoulli(N: int, C: Binomial) -> list:
    mod = C.mod
    res = [C.finv(i + 1) for i in range(N + 1)]
    res = FPS(mod).inv(res, N + 1)
    return [x * C.fac(i) % mod for i, x in enumerate(res)]

def partition(N: int, mod: int) -> list:
    res = [0] * (N + 1)
    res[0] = 1
    for k in range(1, N + 1):
        k1 = k * (3 * k + 1) >> 1
        k2 = k * (3 * k - 1) >> 1
        if k2 > N: break
        if k1 <= N: res[k1] += (-1 if k & 1 else 1)
        if k2 <= N: res[k2] += (-1 if k & 1 else 1)
    return FPS(mod).inv(res)

def montmort(N: int, mod: int) -> list:
    if N <= 1: return [0]
    if N == 2: return [0, 1]
    f = [0] * N
    f[0] = 0; f[1] = tmp = 1
    for i in range(2, N): f[i] = tmp = (tmp + f[i - 2]) * i % mod
    return f
