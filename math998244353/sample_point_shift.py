# my module
from math998244353.ntt import *
# my module
# https://nyaannyaan.github.io/library/fps/sample-point-shift.hpp
def sample_point_shift(y: Vector, t: int, m: int=-1) -> Vector:
    '''
    y: sample point f(0), f(1),... f(N - 1)
    t: shift
    return: f(t + i) for i in range(m)
    '''
    if m == -1: m = len(y)
    k = len(y) - 1
    t %= MOD
    if t <= k:
        ret = [0] * m
        ptr = 0
        for i in range(t, k + 1):
            ret[ptr] = y[i]
            ptr += 1
            if ptr == m: break
        if k + 1 < t + m:
            suf = sample_point_shift(y, k + 1, m - ptr)
            for i in range(k + 1, t + m):
                ret[ptr] = suf[i - k - 1]
                ptr += 1
        return ret
    if t + m > MOD:
        pref = sample_point_shift(y, t, MOD - t)
        suf = sample_point_shift(y, 0, m - len(pref))
        return pref + suf

    finv = [1] * (k + 1)
    d = [0] * (k + 1)
    tmp = 1
    for i in range(2, k + 1): tmp = tmp * i % MOD
    finv[-1] = tmp = modinv(tmp, MOD)
    for i in range(k)[::-1]: finv[i] = tmp = tmp * (i + 1) % MOD
    for i, x in enumerate(y):
        d[i] = (finv[i] * finv[k - i] % MOD) * x % MOD
        if (k - i) & 1: d[i] = -d[i]

    h = [0] * (m + k)
    for i in range(m + k): h[i] = modinv(t - k + i, MOD)

    dh = NTT.multiply(d, h)

    ret = [0] * m
    cur = t
    for i in range(1, k + 1): cur = cur * (t - i) % MOD
    for i in range(m):
        ret[i] = cur * dh[k + i] % MOD
        cur = (cur * (t + i + 1) % MOD) * h[i] % MOD
    return ret
