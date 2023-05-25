# my module
from modulo.binomial import *
from fps.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/sample-point-shift.hpp
def sample_point_shift(y: list, t: int, mod: int, m: int=-1) -> list:
    if m == -1: m == len(y)
    T = t
    k = len(y) - 1
    T %= mod
    if T <= k:
        ret = [0] * m
        ptr = 0
        for i in range(T, k + 1):
            ret[ptr] = y[i]
            ptr += 1
            if ptr == m: break
        if k + 1 < T + m:
            suf = sample_point_shift(y, k + 1, mod, m - ptr)
            for i in range(k + 1, T + m):
                ret[ptr] = suf[i - k - 1]
                ptr += 1
        return ret
    if T + m > mod:
        pref = sample_point_shift(y, T, mod, mod - T)
        suf = sample_point_shift(y, 0, mod, m - len(pref))
        return pref + suf

    finv = [1] * (k + 1)
    d = [0] * (k + 1)
    tmp = 1
    for i in range(2, k + 1): tmp = tmp * i % mod
    finv[-1] = tmp = modinv(tmp, mod)
    for i in range(k)[::-1]: finv[i] = tmp = tmp * (i + 1) % mod
    for i, x in enumerate(y):
        d[i] = (finv[i] * finv[k - i] % mod) * x % mod
        if (k - i) & 1: d[i] = -d[i]

    h = [0] * (m + k)
    for i in range(m + k): h[i] = modinv(T - k + i, mod)

    dh = FPS(mod).mul(d, h)

    ret = [0] * m
    cur = T
    for i in range(1, k + 1): cur = cur * (T - i) % mod
    for i in range(m):
        ret[i] = cur * dh[k + i] % mod
        cur = (cur * (T + i + 1) % mod) * h[i] % mod
    return ret
