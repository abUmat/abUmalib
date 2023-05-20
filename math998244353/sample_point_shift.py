# my module
from modulo.binomial import *
from math998244353.ntt import *
# my module
# https://nyaannyaan.github.io/library/fps/sample-point-shift.hpp
def sample_point_shift(y: list, t: int, m: int=-1) -> list:
    if m == -1: m == len(y)
    T = t
    k = len(y) - 1
    T %= MOD
    if T <= k:
        ret = [0] * m
        ptr = 0
        for i in range(T, k + 1):
            ret[ptr] = y[i]
            ptr += 1
            if ptr == m: break
        if k + 1 < T + m:
            suf = sample_point_shift(y, k + 1, m - ptr)
            for i in range(k + 1, T + m):
                ret[ptr] = suf[i - k - 1]
                ptr += 1
        return ret
    if T + m > MOD:
        pref = sample_point_shift(y, T, MOD - T)
        suf = sample_point_shift(y, 0, m - len(pref))
        return pref + suf

    finv = [1] * (k + 1)
    d = [0] * (k + 1)
    tmp = 1
    for i in range(2, k + 1): tmp = tmp * i % MOD
    finv[-1] = tmp = pow(tmp, MOD - 2, MOD)
    for i in range(k)[::-1]: finv[i] = tmp = tmp * (i + 1) % MOD
    for i, x in enumerate(y):
        d[i] = (finv[i] * finv[k - i] % MOD) * x % MOD
        if (k - i) & 1: d[i] = -d[i]

    h = [0] * (m + k)
    for i in range(m + k): h[i] = pow(T - k + i, MOD - 2, MOD)

    dh = NTT.multiply(d, h)

    ret = [0] * m
    cur = T
    for i in range(1, k + 1): cur = cur * (T - i) % MOD
    for i in range(m):
        ret[i] = cur * dh[k + i] % MOD
        cur = (cur * (T + i + 1) % MOD) * h[i] % MOD
    return ret