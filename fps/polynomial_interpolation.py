# my module
from fps.multieval import *
# my module
# https://nyaannyaan.github.io/library/fps/polynomial-interpolation.hpp
def polynomial_interpolation(xs: list, ys: list, mod: int) -> list:
    assert(len(xs) == len(ys))
    ptree = ProductTree(xs, mod)
    fps = FPS(mod)
    w = fps.diff(ptree.buf[1])
    vs = inner_multipoint_evaluation(w, xs, ptree)

    def rec(idx: int) -> list:
        if idx >= ptree.N:
            if idx - ptree.N < len(xs):
                return [ys[idx - ptree.N] * pow(vs[idx - ptree.N], mod - 2, mod) % mod]
            else:
                return [1]
        if not ptree.buf[idx << 1 | 0]: return []
        if not ptree.buf[idx << 1 | 1]: return rec(idx << 1 | 0)
        return fps.add(fps.mul(rec(idx << 1 | 0), ptree.buf[idx << 1 | 1]), fps.mul(rec(idx << 1 | 1), ptree.buf[idx << 1 | 0]))
    return rec(1)
