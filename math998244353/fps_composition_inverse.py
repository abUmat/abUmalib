# my module
from math998244353.fps_composition import *
# my module
# https://judge.yosupo.jp/submission/139183
# abst. https://maspypy.com/多項式・形式的べき級数-高速に計算できるもの#toc9
def composition_inverse(f: Poly, deg: int=-1) -> Poly:
    '''return: g s.t. f(g(x)) == g(f(x)) == x'''
    deg = len(f) if deg == -1 else deg
    dfdx = FPS.diff(f)
    f = [-x for x in f]
    res = [0]
    m = 1
    while m < deg:
        m <<= 1
        cf0, cf1 = composition_multi([f, dfdx], res, m)
        cf0[1] += 1
        tmp = NTT.multiply(cf0, FPS.inv(cf1, m))
        res[m >> 1:] = tmp[m >> 1:min(deg, m)]
    return res
