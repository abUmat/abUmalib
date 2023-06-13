# my module
from math998244353.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/mod-pow.hpp
def mod_pow(k: int, base: Poly, d: Poly) -> Poly:
    assert(d)
    inv = FPS.inv(d[::-1])
    def quo(poly: Poly) -> Poly:
        if len(poly) < len(d): return []
        n = len(poly) - len(d) + 1
        return NTT.multiply(poly[:len(poly) - n - 1:-1], inv[:n])[n - 1::-1]

    res = [1]
    b = base[:]
    while k:
        if k & 1:
            res = NTT.multiply(res, b)
            res = FPS.sub(res, NTT.multiply(quo(res), d))
            FPS.shrink(res)
        b = NTT.pow2(b)
        b = FPS.sub(b, NTT.multiply(quo(b), d))
        FPS.shrink(b)
        k >>= 1
        # assert(len(b) + 1 <= len(d))
        # assert(len(res) + 1 <= len(d))
    return res
