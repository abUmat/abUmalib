# my module
from fps.fps import *
from modulo.binomial import *
# my module
# https://nyaannyaan.github.io/library/fps/taylor-shift.hpp
def taylor_shift(f: list, a: int, C: Binomial):
    mod = C.mod
    n = len(f)
    res = [x * C.fac(i) % mod for i, x in enumerate(f)]
    res.reverse()
    g = [0] * n
    g[0] = tmp = 1
    for i in range(1, n): g[i] = tmp = (tmp * a % mod) * C.inv(i) % mod
    res = FPS(mod).mul(res, g)[:n]
    res.reverse()
    return [x * C.finv(i) % mod for i, x in enumerate(res)]
