# my module
from math998244353.ntt import *
# my module
# https://nyaannyaan.github.io/library/ntt/relaxed-convolution.hpp
class RelaxedConvolution:
    def __init__(self, n: int) -> None:
        self.n = n
        self.q = 0
        self.a = [0] * (n + 1)
        self.b = [0] * (n + 1)
        self.c = [0] * (n + 1)
        self.aa: List[Poly] = []
        self.bb: List[Poly] = []

    def get(self, x: int, y: int) -> int:
        '''
        x: a[q]
        y: b[q]
        return: c[q]
        '''
        q, n = self.q, self.n
        a, b, c = self.a, self.b, self.c
        aa, bb = self.aa, self.bb
        assert(q <= n)
        a[q] = x; b[q] = y
        c[q] += a[q] * b[0] + (b[q] * a[0] if q else 0)
        c[q] %= MOD

        def precalc(lg: int) -> None:
            if len(aa) <= lg:
                aa[len(aa):] = [0] * (lg + 1 - len(aa))
                bb[len(bb):] = [0] * (lg + 1 - len(bb))
            if aa[lg]: return
            d = 1 << lg
            s = a[:d << 1]
            t = b[:d << 1]
            NTT.ntt(s); NTT.ntt(t)
            aa[lg] = s; bb[lg] = t

        self.q += 1; q += 1
        if q > n:
            return c[q - 1]

        f: Poly = []
        g: Poly = []
        for lg in range(q.bit_length()):
            d = 1 << lg
            if q & ((d << 1) - 1) != d:
                continue
            if q == d:
                f = a[:d] + [0] * d
                g = b[:d] + [0] * d
                NTT.ntt(f); NTT.ntt(g)
                f = [f[i] * y % MOD for i, y in enumerate(g)]
                NTT.intt(f)
                for i in range(q, min(q + d, n + 1)):
                    c[i] += f[d + i - q]
                    c[i] %= MOD
            else:
                precalc(lg)
                f = [a[q - d + i] for i in range(d)] + [0] * d
                g = [b[q - d + i] for i in range(d)] + [0] * d
                NTT.ntt(f); NTT.ntt(g)
                s = aa[lg]; t = bb[lg]
                for i in range(d << 1):
                    f[i] = (f[i] * t[i] + g[i] * s[i]) % MOD
                NTT.intt(f)
                for i in range(q, min(q + d, n + 1)):
                    c[i] += f[d + i - q]
                    c[i] %= MOD
        return c[q - 1]
