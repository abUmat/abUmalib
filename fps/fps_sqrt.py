# my module
from fps.fps import *
from modulo.mod_sqrt import *
# my module
# https://nyaannyaan.github.io/library/fps/fps-sqrt.hpp
def fps_sqrt(f: Poly, mod: int, deg=-1) -> Poly:
    '''return: g s.t. g(x) = sqrt(f(x)) (mod x ** deg)'''
    if deg == -1: deg = len(f)
    if len(f) == 0: return [0] * deg
    if f[0] == 0:
        for i in range(1, len(f)):
            if f[i] != 0:
                if i & 1: return []
                if deg - i // 2 <= 0: break
                ret = fps_sqrt(f[i:], mod, deg - i // 2)
                if not ret: return []
                ret[:0] = [0] * (i >> 1)
                FPS.resize(ret, deg)
                return ret
        return [0] * deg
    sqr = mod_sqrt(f[0], mod)
    if sqr == -1: return []
    ret = [sqr]
    inv2 = pow(2, mod - 2, mod)
    i = 1
    fps = FPS(mod)
    while i < deg:
        i <<= 1
        ret = fps.mul(fps.add(ret, fps.mul(f[:i], fps.inv(ret, i))), inv2)
    return ret[:deg]
