# my module
from modulo.mod_sqrt import *
from math998244353.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/fps-sqrt.hpp.html
def fps_sqrt(f: Poly, deg=-1) -> Poly:
    '''return: g s.t. g(x) = sqrt(f(x)) (mod x ** deg)'''
    if deg == -1: deg = len(f)
    if len(f) == 0: return [0] * deg
    if f[0] == 0:
        for i in range(1, len(f)):
            if f[i] != 0:
                if i & 1: return []
                if deg - i // 2 <= 0: break
                ret = fps_sqrt(f[i:], deg - i // 2)
                if not ret: return []
                ret[:0] = [0] * (i >> 1)
                FPS.resize(ret, deg)
                return ret
        return [0] * deg
    sqr = mod_sqrt(f[0], MOD)
    if sqr == -1: return []
    ret = [sqr]
    inv2 = 499122177 # inv2W * 2 == 1 (mod 998244353)
    i = 1
    while i < deg:
        i <<= 1
        ret = FPS.mul(FPS.add(ret, NTT.multiply(f[:i], FPS.inv(ret, i))), inv2)
    return ret[:deg]