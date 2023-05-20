# my module
from fps.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/multipoint-evaluation.hpp
class ProductTree:
    def __init__(self, xs: list, mod: int) -> None:
        self.mod = mod
        self.xs = xs
        self.xsz = xsz = len(xs)
        N = 1
        while N < xsz: N <<= 1
        self.N = N
        self.buf = [[] for _ in range(N << 1)]
        self.l = [xsz] * (N << 1)
        self.r = [xsz] * (N << 1)
        ntt = FPS(mod).ntt
        if not ntt: self.build()
        else: self.build_ntt(ntt)

    def build(self) -> None:
        xsz, N = self.xsz, self.N
        xs, l, r, buf = self.xs, self.l, self.r, self.buf
        for i in range(xsz):
            l[i + N] = i
            r[i + N] = i + 1
            buf[i + N] = [-xs[i], 1]
        for i in range(N - 1, 0, -1):
            l[i] = l[i << 1 | 0]
            r[i] = r[i << 1 | 1]
            if not buf[i << 1 | 0]: continue
            if not buf[i << 1 | 1]:
                buf[i] = buf[i << 1 | 0][::]
                continue
            buf[i] = buf[i << 1 | 0] * buf[i << 1 | 1]

    def build_ntt(self, ntt) -> None:
        mod, xsz, N = self.mod, self.xsz, self.N
        xs, l, r, buf = self.xs, self.l, self.r, self.buf
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
                ntt.ntt_doubling(buf[i])
                f = buf[i << 1 | 1][::]
                ntt.ntt_doubling(f)
            else:
                buf[i] = buf[i << 1 | 0][::]
                ntt.ntt_doubling(buf[i])
                f = buf[i << 1 | 1][::]
                ntt.intt(f)
                FPS.resize(f, len(buf[i]))
                ntt.ntt(f)
            for j in range(len(buf[i])): buf[i][j] = buf[i][j] * f[j] % mod
        for i in range(N << 1):
            ntt.intt(buf[i])
            FPS.shrink(buf[i])

def inner_multipoint_evaluation(f: list, xs: list, ptree: ProductTree):
    ret = []
    fps = FPS(ptree.mod)
    def rec(a: list, idx: int) -> None:
        if ptree.l[idx] == ptree.r[idx]: return
        a = fps.modulo(a, ptree.buf[idx])
        if len(a) <= 64:
            for i in range(ptree.l[idx], ptree.r[idx]): ret.append(fps.eval(a, xs[i]))
            return
        rec(a, idx << 1 | 0)
        rec(a, idx << 1 | 1)
    rec(f, 1)
    return ret

def multipoint_evaluation(f: list, xs: list, mod: int) -> list:
    if not f or not xs: return [0] * len(xs)
    return inner_multipoint_evaluation(f, xs, ProductTree(xs, mod))
