# my module
from modulo.mod_sqrt import *
from math998244353.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/fps-sqrt.hpp.html
def fps_sqrt(a: list, deg=-1) -> list:
    if deg == -1: deg = len(a)
    if len(a) == 0: return [0] * deg
    if a[0] == 0:
        for i in range(1, len(a)):
            if a[i] != 0:
                if i & 1: return []
                if deg - i // 2 <= 0: break
                ret = fps_sqrt(a[i:], deg - i // 2)
                if not ret: return []
                ret[:0] = [0] * (i >> 1)
                if len(ret) < deg: ret[len(ret):] = [0] * (deg - len(ret))
                return ret
        return [0] * deg
    sqr = mod_sqrt(a[0], MOD)
    if sqr == -1: return []
    ret = [sqr]
    inv2 = 499122177
    i = 1
    while i < deg:
        i <<= 1
        ret = FPS.mul(FPS.add(ret, NTT.multiply(a[:i], FPS.inv(ret, i))), inv2)
    return ret[:deg]