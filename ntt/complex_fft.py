# https://judge.yosupo.jp/submission/46633
# cooley_tukey ?
# maybe https://nyaannyaan.github.io/library/ntt/complex-fft.hpp
from math import pi, sin, cos
class CooleyTukey:
    wr = [0] * (1 << 20)
    wi = [0] * (1 << 20)
    baser = [0] * 20
    basei = [0] * 20
    isbuilt = 0
    def __init__(self, k: int=20) -> None:
        self.setw(k)
        self.isbuilt = 1

    @staticmethod
    def mul(xr: float, xi: float, yr: float, yi: float) -> tuple:
        return xr * yr - xi * yi, xr * yi + yr * xi

    def genw(self, i: int, b: int, zr: float, zi: float) -> None:
        if b == -1:
            self.wr[i] = zr
            self.wi[i] = zi
        else:
            self.genw(i, b - 1, zr, zi)
            wr, wi = self.baser[b], self.basei[b]
            self.genw(i | (1 << b), b - 1, zr * wr - zi * wi, zr * wi + zi * wr)

    def setw(self, k: int) -> None:
        k -= 1
        arg = pi / (1 << k)
        i = 0
        j = 1 << (k - 1)
        while j:
            self.baser[i] = cos(arg * j)
            self.basei[i] = sin(arg * j)
            i += 1
            j >>= 1
        self.genw(0, k - 1, 1, 0)

    def fft(self, ar: list, ai: list, k: int) -> None:
        if k == 0: return
        if k == 1:
            ar[0], ar[1] = ar[0] + ar[1], ar[0] - ar[1]
            ai[0], ai[1] = ai[0] + ai[1], ai[0] - ai[1]
            return
        if k & 1:
            v = 1 << (k - 1)
            for j in range(v):
                ar[j], ar[j + v] = ar[j] + ar[j + v], ar[j] - ar[j + v]
                ai[j], ai[j + v] = ai[j] + ai[j + v], ai[j] - ai[j + v]
        u = 1 << (k & 1)
        v = 1 << (k - 2 - (k & 1))
        wr1, wi1 = self.wr[1], self.wi[1]
        while v:
            for j0 in range(v):
                t0r = ar[j0]; t0i = ai[j0]
                t1r = ar[j0 + v]; t1i = ai[j0 + v]
                t2r = ar[j0 + v * 2]; t2i = ai[j0 + v * 2]
                t3r = ar[j0 + v * 3]; t3i = ai[j0 + v * 3]
                t1m3r, t1m3i = self.mul(t1r - t3r, t1i - t3i, wr1, wi1)
                ar[j0] = (t0r + t2r) + (t1r + t3r); ai[j0] = (t0i + t2i) + (t1i + t3i)
                ar[j0 + v] = (t0r + t2r) - (t1r + t3r); ai[j0 + v] = (t0i + t2i) - (t1i + t3i)
                ar[j0 + v * 2] = (t0r - t2r) + t1m3r; ai[j0 + v * 2] = (t0i - t2i) + t1m3i
                ar[j0 + v * 3] = (t0r - t2r) - t1m3r; ai[j0 + v * 3] = (t0i - t2i) - t1m3i

            for jh in range(1, u):
                p = jh * v * 4
                Wr = self.wr[jh]; Wi = self.wi[jh]
                Xr = self.wr[jh << 1]; Xi = self.wi[jh << 1]
                WXr, WXi = self.mul(Wr, Wi, Xr, Xi)
                for offset in range(v):
                    t0r = ar[p + offset]; t0i = ai[p + offset]
                    t1r, t1i = self.mul(ar[p + offset + v], ai[p + offset + v], Xr, Xi)
                    t2r, t2i = self.mul(ar[p + offset + v * 2], ai[p + offset + v * 2], Wr, Wi)
                    t3r, t3i = self.mul(ar[p + offset + v * 3], ai[p + offset + v * 3], WXr, WXi)
                    t1m3r, t1m3i = self.mul(t1r - t3r, t1i - t3i, wr1, wi1)
                    ar[p + offset] = (t0r + t2r) + (t1r + t3r); ai[p + offset] = (t0i + t2i) + (t1i + t3i)
                    ar[p + offset + v] = (t0r + t2r) - (t1r + t3r); ai[p + offset + v] = (t0i + t2i) - (t1i + t3i)
                    ar[p + offset + v * 2] = (t0r - t2r) + t1m3r; ai[p + offset + v * 2] = (t0i - t2i) + t1m3i
                    ar[p + offset + v * 3] = (t0r - t2r) - t1m3r; ai[p + offset + v * 3] = (t0i - t2i) - t1m3i
            u <<= 2
            v >>= 2

    def ifft(self, ar: list, ai: list, k: int) -> None:
        if k == 0: return
        if k == 1:
            ar[0], ar[1] = ar[0] + ar[1], ar[0] - ar[1]
            ai[0], ai[1] = ai[0] + ai[1], ai[0] - ai[1]
            return
        u = 1 << (k - 2)
        v = 1
        wr1, mwi1 = self.wr[1], -self.wi[1]
        while u:
            for j0 in range(v):
                t0r = ar[j0]; t0i = ai[j0]
                t1r = ar[j0 + v]; t1i = ai[j0 + v]
                t2r = ar[j0 + v * 2]; t2i = ai[j0 + v * 2]
                t3r = ar[j0 + v * 3]; t3i = ai[j0 + v * 3]
                t2m3r, t2m3i = self.mul(t2r - t3r, t2i - t3i, wr1, mwi1)
                ar[j0] = (t0r + t1r) + (t2r + t3r); ai[j0] = (t0i + t1i) + (t2i + t3i)
                ar[j0 + v * 2] = (t0r + t1r) - (t2r + t3r); ai[j0 + v * 2] = (t0i + t1i) - (t2i + t3i)
                ar[j0 + v] = (t0r - t1r) + t2m3r; ai[j0 + v] = (t0i - t1i) + t2m3i
                ar[j0 + v * 3] = (t0r - t1r) - t2m3r; ai[j0 + v * 3] = (t0i - t1i) - t2m3i
            for jh in range(1, u):
                p = jh * v * 4
                Wr = self.wr[jh]; Wi = -self.wi[jh]
                Xr = self.wr[(jh << 1) + 0]; Xi = -self.wi[(jh << 1) + 0]
                Yr = self.wr[(jh << 1) + 1]; Yi = -self.wi[(jh << 1) + 1]
                for offset in range(v):
                    t0r = ar[p + offset]; t0i = ai[p + offset]
                    t1r = ar[p + offset + v]; t1i = ai[p + offset + v]
                    t2r = ar[p + offset + v * 2]; t2i = ai[p + offset + v * 2]
                    t3r = ar[p + offset + v * 3]; t3i = ai[p + offset + v * 3]
                    t0m1r, t0m1i = self.mul(t0r - t1r, t0i - t1i, Xr, Xi)
                    t2m3r, t2m3i = self.mul(t2r - t3r, t2i - t3i, Yr, Yi)
                    ar[p + offset] = (t0r + t1r) + (t2r + t3r); ai[p + offset] = (t0i + t1i) + (t2i + t3i)
                    ar[p + offset + v] = t0m1r + t2m3r; ai[p + offset + v] = t0m1i + t2m3i
                    ar[p + offset + v * 2], ai[p + offset + v * 2] = self.mul((t0r + t1r) - (t2r + t3r), (t0i + t1i) - (t2i + t3i), Wr, Wi)
                    ar[p + offset + v * 3], ai[p + offset + v * 3] = self.mul(t0m1r - t2m3r, t0m1i - t2m3i, Wr, Wi)
            u >>= 2
            v <<= 2
        if k & 1:
            u = 1 << (k - 1)
            for j in range(u):
                ar[j], ar[j + u] = ar[j] + ar[j + u], ar[j] - ar[j + u]
                ai[j], ai[j + u] = ai[j] + ai[j + u], ai[j] - ai[j + u]

    def fft_real(self, ALr: list, ALi: list, AHr: list, AHi: list, k: int) -> None:
        self.fft(ALr, ALi, k)
        AHr[0] = ALi[0] * 2; AHi[0] = 0
        ALr[0] = ALr[0] * 2; ALi[0] = 0
        AHr[1] = ALi[1] * 2; AHi[1] = 0
        ALr[1] = ALr[1] * 2; ALi[1] = 0
        i = 2; y = 2
        while y < 1 << k:
            while i < y << 1:
                j = i ^ (y - 1)
                AHr[i] = ALi[j] + ALi[i]; AHi[i] = ALr[j] - ALr[i]
                ALr[i] = ALr[j] + ALr[i]; ALi[i] = -ALi[j] + ALi[i]
                AHr[j] = AHr[i]; AHi[j] = -AHi[i]
                ALr[j] = ALr[i]; ALi[j] = -ALi[i]
                i += 2
            y <<= 1

    def karatsuba(self, a: list, b: list, mod: int) -> list:
        B = 32000
        bbmod = B * B % mod
        l = len(a) + len(b) - 1
        k = 2; M = 4
        while M < l:
            M <<= 1
            k += 1
        if not self.isbuilt:
            self.setw(k)
        alr = [float()] * M
        ali = [float()] * M
        ahr = [float()] * M
        ahi = [float()] * M
        blr = [float()] * M
        bli = [float()] * M
        bhi = [float()] * M
        bhr = [float()] * M
        for i, x in enumerate(a):
            quo, rem = divmod(x, B)
            alr[i], ali[i] = float(rem), float(quo)
        for i, x in enumerate(b):
            quo, rem = divmod(x, B)
            blr[i], bli[i] = float(rem), float(quo)

        self.fft_real(alr, ali, ahr, ahi, k)
        self.fft_real(blr, bli, bhr, bhi, k)

        for i in range(M):
            alri = alr[i]; alii = ali[i]
            mahii = -ahi[i]; ahri = ahr[i]
            tmp1r, tmp1i = self.mul(alri, alii, blr[i], bli[i])
            tmp2r, tmp2i = self.mul(mahii, ahri, bhr[i], bhi[i])
            tmp3r, tmp3i = self.mul(alri, alii, bhr[i], bhi[i])
            tmp4r, tmp4i = self.mul(mahii, ahri, blr[i], bli[i])
            blr[i] = tmp1r + tmp2r; bli[i] = tmp1i + tmp2i
            bhr[i] = tmp3r + tmp4r; bhi[i] = tmp3i + tmp4i

        self.ifft(blr, bli, k)
        self.ifft(bhr, bhi, k)

        u = [0] * l
        im = float(1 / (4 * M))
        for i in range(l):
            x1 = round(blr[i] * im) % mod
            x2 = (round(bhr[i] * im) + round(bhi[i] * im)) % mod * B % mod
            x3 = round(bli[i] * im) % mod * bbmod % mod
            x = x1 + x2 + x3
            if x >= mod: x -= mod
            if x >= mod: x -= mod
            u[i] = x
        return u

    def karatsuba_pow2(self, a: list, mod: int) -> list:
        B = 32000
        l = len(a) * 2 - 1
        k = 2; M = 4
        while M < l:
            M <<= 1
            k += 1
        self.setw(k)
        alr = [float()] * M
        ali = [float()] * M
        ahr = [float()] * M
        ahi = [float()] * M
        for i, x in enumerate(a):
            quo, rem = divmod(x, B)
            alr[i], ali[i] = float(rem), float(quo)

        self.fft_real(alr, ali, ahr, ahi, k)

        for i in range(M):
            tmp1r = alr[i]; tmp1i = ali[i]
            tmp2r = -ahi[i]; tmp2i = ahr[i]
            tmp3r = tmp1r; tmp3i = tmp1i
            tmp4r = tmp2r; tmp4i = tmp2i
            tmp1r, tmp1i = self.mul(tmp1r, tmp1i, alr[i], ali[i])
            tmp2r, tmp2i = self.mul(tmp2r, tmp2i, ahr[i], ahi[i])
            tmp3r, tmp3i = self.mul(tmp3r, tmp3i, ahr[i], ahi[i])
            tmp4r, tmp4i = self.mul(tmp4r, tmp4i, alr[i], ali[i])
            alr[i] = tmp1r + tmp2r; ali[i] = tmp1i + tmp2i
            ahr[i] = tmp3r + tmp4r; ahi[i] = tmp3i + tmp4i

        self.ifft(alr, ali, k)
        self.ifft(ahr, ahi, k)

        u = [0] * l
        im = float(1 / (4 * M))
        for i in range(l):
            alr[i] *= im; ali[i] *= im
            ahr[i] *= im; ahi[i] *= im
            x1 = round(alr[i]) % mod
            x2 = (round(ahr[i]) + round(ahi[i])) % mod * B % mod
            x3 = round(ali[i]) % mod * (B * B % mod) % mod
            x1 += x2
            if x1 >= mod: x1 -= mod
            x1 += x3
            if x1 >= mod: x1 -= mod
            u[i] = x1
        return u
