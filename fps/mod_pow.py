# my module
from fps.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/mod-pow.hpp
def mod_pow(k: int, base: Poly, d: Poly, mod: int, fps: FPS=None) -> Poly:
    assert(d)
    if not fps: fps = FPS(mod)
    inv = fps.inv(d[::-1])
    def quo(poly: Poly) -> Poly:
        if len(poly) < len(d): return []
        n = len(poly) - len(d) + 1
        return fps.mul(poly[:len(poly) - n - 1:-1], inv[:n])[n - 1::-1]

    res = [1]
    b = base[:]
    while k:
        if k & 1:
            res = fps.mul(res, b)
            res = fps.sub(res, fps.mul(quo(res), d))
            FPS.shrink(res)
        b = fps.mul2(b)
        b = fps.sub(b, fps.mul(quo(b), d))
        FPS.shrink(b)
        k >>= 1
        # assert(len(b) + 1 <= len(d))
        # assert(len(res) + 1 <= len(d))
    return res
