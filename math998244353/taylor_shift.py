# my module
from math998244353.fps import *
from modulo.binomial import *
# my module
# https://nyaannyaan.github.io/library/fps/taylor-shift.hpp
def taylor_shift(f: list, a: int, C: Binomial):
    n = len(f)
    res = [x * C.fac(i) % MOD for i, x in enumerate(f)]
    res.reverse()
    g = [0] * n
    g[0] = tmp = 1
    for i in range(1, n): g[i] = tmp = (tmp * a % MOD) * C.inv(i) % MOD
    res = NTT.multiply(res, g)[:n]
    res.reverse()
    return [x * C.finv(i) % MOD for i, x in enumerate(res)]
