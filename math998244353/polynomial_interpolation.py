# my module
from math998244353.multieval import *
# my module
# https://nyaannyaan.github.io/library/fps/polynomial-interpolation.hpp
def polynomial_interpolation(xs: Vector, ys: Vector) -> Poly:
    '''return: f s.t. f(x[i]) == y[i] for all i'''
    assert(len(xs) == len(ys))
    ptree = ProductTree(xs)
    w = FPS.diff(ptree.buf[1])
    vs = inner_multipoint_evaluation(w, xs, ptree)
    def rec(idx: int) -> list:
        if idx >= ptree.N:
            if idx - ptree.N < len(xs):
                return [ys[idx - ptree.N] * modinv(vs[idx - ptree.N], MOD) % MOD]
            else:
                return [1]
        if not ptree.buf[idx << 1 | 0]: return []
        if not ptree.buf[idx << 1 | 1]: return rec(idx << 1 | 0)
        return FPS.add(NTT.multiply(rec(idx << 1 | 0), ptree.buf[idx << 1 | 1]), NTT.multiply(rec(idx << 1 | 1), ptree.buf[idx << 1 | 0]))
    return rec(1)
