def _ctz(ll):
    cnt = 0
    while not ll & 1:
        ll >>= 1
        cnt += 1
    return cnt

class NTT:
    def __init__(self, MOD) -> None:
        self.MOD = MOD
        self.pr = self._get_pr()
        cnt = _ctz(MOD - 1)
        self.level = cnt
        self.dw = [None] * cnt
        self.dy = [None] * cnt
        self._setwy(cnt)

    def _get_pr(self):
        mod = self.MOD
        ds = [None] * 32
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

    def _setwy(self, k):
        mod = self.MOD
        w, y = [None] * self.level, [None] * self.level
        w[k - 1] = pow(self.pr, (mod - 1) // (1 << k), mod)
        y[k - 1] = pow(w[k - 1], mod - 2, mod)
        for i in range(k - 1)[::-1]:
            w[i] = w[i + 1] * w[i + 1] % mod
            y[i] = y[i + 1] * y[i + 1] % mod
        self.dw[1] = w[1]; self.dy[1] = y[1]; self.dw[2] = w[2]; self.dy[2] = y[2]
        for i in range(3, k):
            self.dw[i] = self.dw[i - 1] * y[i - 2] * w[i] % mod
            self.dy[i] = self.dy[i - 1] * w[i - 2] * y[i] % mod

    def _fft4(self, a, k):
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
                j1 = j0 + v; j2 = j1 + v; j3 = j2 + v
                t0, t1 = a[j0], a[j1]; t2, t3 = a[j2], a[j3]
                t0p2, t1p3 = t0 + t2, t1 + t3; t0m2, t1m3 = t0 - t2, (t1 - t3) * imag % mod
                a[j0], a[j1] = t0p2 + t1p3, t0p2 - t1p3; a[j2], a[j3] = t0m2 + t1m3, t0m2 - t1m3
            ww = 1; xx = self.dw[2]; wx = 1
            for jh in range(4, u, 4):
                ww = xx * xx % mod; wx = ww * xx % mod
                je = jh * v + v
                for j0 in range(jh * v, je):
                    j2 = j0 + v + v
                    t0, t1 = a[j0], a[j0 + v] * xx % mod; t2, t3 = a[j2] * ww % mod, a[j2 + v] * wx % mod
                    t0p2, t1p3 = t0 + t2, t1 + t3; t0m2, t1m3 = t0 - t2, (t1 - t3) * imag % mod
                    a[j0], a[j0 + v] = t0p2 + t1p3, t0p2 - t1p3; a[j2], a[j2 + v] = t0m2 + t1m3, t0m2 - t1m3
                xx = xx * self.dw[_ctz(jh + 4)] % mod
            u <<= 2
            v >>= 2
        for i in range(len(a)): a[i] %= mod

    def _ifft(self, a, k):
        mod = self.MOD
        if len(a) <= 1: return
        if k == 1:
            a[0], a[1] = a[0] + a[1], a[0] - a[1]
            a[0] %= mod; a[1] %= mod
            return
        u = 1 << (k - 2)
        v = 1
        imag = self.dy[1]
        while u:
            for j0 in range(v):
                j1 = j0 + v; j2 = j1 + v; j3 = j2 + v
                t0, t1 = a[j0], a[j1]; t2, t3 = a[j2], a[j3]
                t0p1, t2p3 = t0 + t1, t2 + t3; t0m1, t2m3= t0 - t1, (t2 - t3) * imag % mod
                a[j0], a[j1] = t0p1 + t2p3, t0m1 + t2m3; a[j2], a[j3] = t0p1 - t2p3, t0m1 - t2m3
            ww = 1; xx = self.dy[2]; yy = 1
            u <<= 2
            for jh in range(4, u, 4):
                ww = xx * xx % mod; yy = xx * imag % mod
                je = jh * v + v
                for j0 in range(jh * v, je):
                    j2 = j0 + v + v
                    t0, t1 = a[j0], a[j0 + v]; t2, t3 = a[j2], a[j2 + v]
                    t0p1, t2p3 = t0 + t1, t2 + t3; t0m1, t2m3 = (t0 - t1) * xx % mod, (t2 - t3) * yy % mod
                    a[j0], a[j0 + v] = t0p1 + t2p3, t0m1 + t2m3; a[j2], a[j2 + v] = (t0p1 - t2p3) * ww % mod, (t0m1 - t2m3) * ww % mod
                xx = xx * self.dy[_ctz(jh + 4)] % mod
            u >>= 4
            v <<= 2
        if k & 1:
            u = 1 << (k - 1)
            for j in range(u): a[j], a[j + u] = a[j] + a[j + u], a[j] - a[j + u]
        for i in range(len(a)): a[i] %= mod

    def ntt(self, a):
        if len(a) <= 1: return
        self._fft4(a, _ctz(len(a)))

    def intt(self, a):
        if len(a) <= 1: return
        self._ifft(a, _ctz(len(a)))
        mod = self.MOD
        iv = pow(len(a), mod - 2, mod)
        for i in range(len(a)): a[i] = a[i] * iv % mod

    def multiply(self, a, b):
        mod = self.MOD
        l = len(a) + len(b) - 1
        if min(len(a), len(b)) <= 40:
            s = [0] * l
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    s[i + j] += x * y % mod
            for i in range(l): s[i] %= mod
            return s
        k = 2; M = 4
        while M < l: M <<= 1; k += 1
        self._setwy(k)
        s, t = [0] * M, [0] * M
        for i, x in enumerate(a): s[i] = x
        for i, x in enumerate(b): t[i] = x
        self._fft4(s, k)
        self._fft4(t, k)
        for i, x in enumerate(t): s[i] = s[i] * x % mod
        self._ifft(s, k)
        s = s[:l]
        invm = pow(M, mod - 2, mod)
        for i, x in enumerate(s): s[i] = x * invm % mod
        return s

    def ntt_doubling(self, a):
        mod = self.MOD
        M = len(a)
        self.intt(a)
        r = 1; zeta = pow(self.pr, (mod - 1) // (M << 1), mod)
        for i, x in enumerate(a):
            a[i] = x * r % mod
            r = r * zeta % mod
        self.ntt(a)
