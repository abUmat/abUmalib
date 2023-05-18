# my module
from math998244353.fps import *
# my module
class ProductTree:
    def __init__(self, xs: list) -> None:
        self.xs = xs
        self.xsz = xsz = len(xs)
        N = 1
        while N < xsz: N <<= 1
        self.N = N
        self.buf = buf = [[] for _ in range(N << 1)]
        self.l = l = [xsz] * (N << 1)
        self.r = r = [xsz] * (N << 1)
        f = []
        for i in range(xsz):
            l[i + N] = i
            r[i + N] = i + 1
            buf[i + N] = [-xs[i] + 1, -xs[i] - 1]
        for i in range(N - 1, 0, -1):
            f = []
            l[i] = l[i << 1 | 0]
            r[i] = r[i << 1 | 1]
            if not buf[i << 1 | 0]: continue
            if not buf[i << 1 | 1]:
                buf[i] = buf[i << 1 | 0][::]
                continue
            if len(buf[i << 1 | 0]) == len(buf[i << 1 | 1]):
                buf[i] = buf[i << 1 | 0][::]
                ntt_doubling(buf[i])
                f = buf[i << 1 | 1][::]
                ntt_doubling(f)
            else:
                buf[i] = buf[i << 1 | 0][::]
                ntt_doubling(buf[i])
                f = buf[i << 1 | 1][::]
                intt(f)
                f[len(buf[i]):] = []; f[len(f):] = [0] * (len(buf[i]) - len(f))
                ntt(f)
            for j in range(len(buf[i])): buf[i][j] = buf[i][j] * f[j] % MOD
        for i in range(N << 1):
            intt(buf[i])
            while buf[i] and not buf[i][-1]: buf[i].pop()

def inner_multipoint_evaluation(f: list, xs: list, ptree: ProductTree):
    ret = []
    def rec(a: list, idx: int) -> None:
        if ptree.l[idx] == ptree.r[idx]: return
        a = fps_mod(a, ptree.buf[idx])
        if len(a) <= 64:
            for i in range(ptree.l[idx], ptree.r[idx]): ret.append(fps_eval(a, xs[i]))
            return
        rec(a, idx << 1 | 0)
        rec(a, idx << 1 | 1)
    rec(f, 1)
    return ret

def multipoint_evaluation(f: list, xs: list) -> list:
    if not f or not xs: return [0] * len(xs)
    return inner_multipoint_evaluation(f, xs, ProductTree(xs))
