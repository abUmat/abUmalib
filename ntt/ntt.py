# my module
from gcc_builtins import *
# my module
class NTT:
    def __init__(self, MOD: int) -> None:
        self.MOD = MOD
        self.pr = self._get_pr()
        cnt = ctz(MOD - 1)
        self.level = cnt
        self.dw = [0] * cnt
        self.dy = [0] * cnt
        self._setwy(cnt)

    def _get_pr(self) -> int:
        mod = self.MOD
        ds = [0] * 32
        idx = 0
        m = mod - 1
        for i in range(2, m):
            if i*i > m: break
            if not m % i:
                ds[idx] = i
                idx += 1
                while not m % i: m //= i
        if m != 1:
            ds[idx] = m
            idx += 1
        pr = 2
        while 1:
            flag = 1
            for i in range(idx):
                a = pr; b = (mod - 1) // ds[i]; r = 1
                while b:
                    if b & 1: r = r * a % mod
                    a = a * a % mod
                    b >>= 1
                if r == 1:
                    flag = 0
                    break
            if flag: break
            pr += 1
        return pr

    def _setwy(self, k: int) -> None:
        mod = self.MOD
        w, y = [None] * self.level, [None] * self.level
        w[k - 1] = tmpw = pow(self.pr, (mod - 1) // (1 << k), mod)
        y[k - 1] = tmpy = pow(w[k - 1], mod - 2, mod)
        for i in range(k - 1)[::-1]:
            w[i] = tmpw = tmpw * tmpw % mod
            y[i] = tmpy = tmpy * tmpy % mod
        self.dw[1] = w[1]; self.dy[1] = y[1]; self.dw[2] = tmpdw = w[2]; self.dy[2] = tmpdy = y[2]
        for i in range(3, k):
            self.dw[i] = tmpdw = (tmpdw * y[i - 2] % mod) * w[i] % mod
            self.dy[i] = tmpdy = (tmpdy * w[i - 2] % mod) * y[i] % mod

    def _fft(self, a: list, k: int) -> None:
        mod = self.MOD
        if len(a) <= 1: return
        if k == 1:
            a[0], a[1] = a[0] + a[1], a[0] - a[1]
            a[0] %= mod; a[1] %= mod
            return
        if k & 1:
            v = 1 << (k - 1)
            for j in range(v): a[j], a[j + v] = a[j] + a[j + v], a[j] - a[j + v]
        u = 1 << (2 + (k & 1))
        v = 1 << (k - 2 - (k & 1))
        imag = self.dw[1]
        while v:
            for j0 in range(0, v):
                t0 = a[j0]
                t1 = a[j0 + v]
                t2 = a[j0 + v * 2]
                t3 = a[j0 + v * 3]
                t1m3 = (t1 - t3) * imag % mod
                a[j0] = t0 + t1 + t2 + t3
                a[j0 + v] = t0 - t1 + t2 - t3
                a[j0 + v * 2] = t0 - t2 + t1m3
                a[j0 + v * 3] = t0 - t2 - t1m3
            ww = 1; xx = self.dw[2]; wx = 1
            for jh in range(4, u, 4):
                ww = xx * xx % mod; wx = ww * xx % mod
                for j0 in range(jh * v, jh * v + v):
                    t0 = a[j0]
                    t1 = a[j0 + v] * xx % mod
                    t2 = a[j0 + v * 2] * ww % mod
                    t3 = a[j0 + v * 3] * wx % mod
                    t1m3 = (t1 - t3) * imag % mod
                    a[j0] = t0 + t1 + t2 + t3
                    a[j0 + v] = t0 - t1 + t2 - t3
                    a[j0 + v * 2] = t0 - t2 + t1m3
                    a[j0 + v * 3] = t0 - t2 - t1m3
                xx = xx * self.dw[ctz(jh + 4)] % mod
            u <<= 2
            v >>= 2
        for i, x in enumerate(a): a[i] = x % mod

    def _ifft(self, a: list, k: int) -> None:
        mod = self.MOD
        if len(a) <= 1: return
        if k == 1:
            a[0], a[1] = (a[0] + a[1]) % mod, (a[0] - a[1]) % mod
            return
        u = 1 << (k - 2)
        v = 1
        imag = self.dy[1]
        while u:
            for j0 in range(v):
                t0 = a[j0]
                t1 = a[j0 + v]
                t2 = a[j0 + v * 2]
                t3 = a[j0 + v * 3]
                t2m3 = (t2 - t3) * imag % mod
                a[j0] = t0 + t1 + t2 + t3
                a[j0 + v] = t0 - t1 + t2m3
                a[j0 + v * 2] = t0 + t1 - t2 - t3
                a[j0 + v * 3] = t0 - t1 - t2m3
            ww = 1; xx = self.dy[2]; yy = 1
            u <<= 2
            for jh in range(4, u, 4):
                ww = xx * xx % mod; yy = xx * imag % mod
                for j0 in range(jh * v, jh * v + v):
                    t0 = a[j0]
                    t1 = a[j0 + v]
                    t2 = a[j0 + v * 2]
                    t3 = a[j0 + v * 3]
                    t0m1 = (t0 - t1) * xx % mod
                    t2m3 = (t2 - t3) * yy % mod
                    a[j0] = t0 + t1 + t2 + t3
                    a[j0 + v] = t0m1 + t2m3
                    a[j0 + v * 2] = (t0 + t1 - t2 - t3) * ww % mod
                    a[j0 + v * 3] = (t0m1 - t2m3) * ww % mod
                xx = xx * self.dy[ctz(jh + 4)] % mod
            u >>= 4
            v <<= 2
        if k & 1:
            u = 1 << (k - 1)
            for j in range(u):
                l, r = a[j], a[j + u]
                a[j], a[j + u] = l + r, l - r
        for i, x in enumerate(a): a[i] = x % mod

    def ntt(self, a: list) -> None:
        if len(a) <= 1: return
        self._fft(a, ctz(len(a)))

    def intt(self, a: list) -> None:
        if len(a) <= 1: return
        self._ifft(a, ctz(len(a)))
        mod = self.MOD
        iv = pow(len(a), mod - 2, mod)
        for i, x in enumerate(a): a[i] = x * iv % mod

    def multiply(self, a: list, b: list) -> list:
        mod = self.MOD
        l = len(a) + len(b) - 1
        if min(len(a), len(b)) <= 60:
            s = [0] * l
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    s[i + j] += x * y
            return [x % mod for x in s]
        k = 2; M = 4
        while M < l: M <<= 1; k += 1
        self._setwy(k)
        s = a + [0] * (M - len(a))
        t = b + [0] * (M - len(b))
        self._fft(s, k)
        self._fft(t, k)
        for i, x in enumerate(t): s[i] = s[i] * x % mod
        self._ifft(s, k)
        s[l:] = []
        invm = pow(M, mod - 2, mod)
        return [x * invm % mod for x in s]

    def pow2(self, a: list) -> list:
        mod = self.MOD
        l = (len(a) << 1) - 1
        if len(a) <= 40:
            s = [0] * l
            for i, x in enumerate(a):
                for j, y in enumerate(a):
                    s[i + j] += x * y
            return [x % mod for x in s]
        k = 2; M = 4
        while M < l: M <<= 1; k += 1
        self._setwy(k)
        s = a + [0] * (M - len(a))
        self._fft(s, k)
        for i, x in enumerate(s): s[i] = x * x % mod
        self._ifft(s, k)
        s[l:] = []
        invm = pow(M, mod - 2, mod)
        return [x * invm % mod for x in s]

    def ntt_doubling(self, a: list) -> None:
        mod = self.MOD
        M = len(a)
        b = a[:]
        self.intt(b)
        r = 1; zeta = pow(self.pr, (mod - 1) // (M << 1), mod)
        for i, x in enumerate(b):
            b[i] = x * r % mod
            r = r * zeta % mod
        self.ntt(b)
        a += b
