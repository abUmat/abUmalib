# my module
from fps.fps import *
from modulo.mod_sqrt import *
# my module
def fps_sqrt(a: list, mod: int, deg: int=-1) -> list:
    if deg == -1: deg = len(a)
    if len(a) == 0: return [0] * deg
    if a[0] == 0:
        for i in range(1, len(a)):
            if a[i] != 0:
                if i & 1: return []
                if deg - i // 2 <= 0: break
                ret = fps_sqrt(a[i:], mod, deg - i // 2)
                if not ret: return []
                ret[:0] = [0] * (i >> 1)
                FPS.resize(ret, deg)
                return ret
        return [0] * deg
    sqr = mod_sqrt(a[0], mod)
    if sqr == -1: return []
    ret = [sqr]
    inv2 = pow(2, mod - 2, mod)
    i = 1
    fps = FPS(mod)
    while i < deg:
        i <<= 1
        ret = fps.mul(fps.add(ret, fps.mul(a[:i], fps.inv(ret, i))), inv2)
    return ret[:deg]
