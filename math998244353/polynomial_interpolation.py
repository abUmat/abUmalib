# my module
from math998244353.multieval import *
# my module
def polynomial_interpolation(xs: list, ys: list) -> list:
    assert(len(xs) == len(ys))
    ptree = ProductTree(xs)
    w = fps_diff(ptree.buf[1])
    vs = inner_multipoint_evaluation(w, xs, ptree)
    def rec(idx: int) -> list:
        if idx >= ptree.N:
            if idx - ptree.N < len(xs):
                return [ys[idx - ptree.N] * pow(vs[idx - ptree.N], MOD - 2, MOD) % MOD]
            else:
                return [1]
        if not ptree.buf[idx << 1 | 0]: return []
        if not ptree.buf[idx << 1 | 1]: return rec(idx << 1 | 0)
        return fps_add(multiply(rec(idx << 1 | 0), ptree.buf[idx << 1 | 1]), multiply(rec(idx << 1 | 1), ptree.buf[idx << 1 | 0]))
    return rec(1)
