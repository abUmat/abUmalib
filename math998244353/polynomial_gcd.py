# my module
from math998244353.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/polynomial-gcd.hpp
class Mat:
    def __init__(self, a00: list, a01: list, a10: list, a11: list) -> None:
        self.arr = [a00, a01, a10, a11]

    def __mul__(self, r):
        a00, a01, a10, a11 = self.arr
        if type(r) is Mat:
            ra00, ra01, ra10, ra11 = r.arr
            A00 = FPS.add(NTT.multiply(a00, ra00), NTT.multiply(a01, ra10))
            A01 = FPS.add(NTT.multiply(a00, ra01), NTT.multiply(a01, ra11))
            A10 = FPS.add(NTT.multiply(a10, ra00), NTT.multiply(a11, ra10))
            A11 = FPS.add(NTT.multiply(a10, ra01), NTT.multiply(a11, ra11))
            FPS.shrink(A00); FPS.shrink(A01); FPS.shrink(A10); FPS.shrink(A11)
            return Mat(A00, A01, A10, A11)
        b0 = FPS.add(NTT.multiply(a00, r[0]), NTT.multiply(a01, r[1]))
        b1 = FPS.add(NTT.multiply(a10, r[0]), NTT.multiply(a11, r[1]))
        FPS.shrink(b0); FPS.shrink(b1)
        return [b0, b1]

    @staticmethod
    def I():
        return Mat([1], [], [], [1])

def inner_naive_gcd(m: Mat, p: list) -> None:
    quo, rem = FPS.divmod(p[0], p[1])
    b10 = FPS.sub(m.arr[0], NTT.multiply(m.arr[2], quo))
    b11 = FPS.sub(m.arr[1], NTT.multiply(m.arr[3], quo))
    FPS.shrink(rem); FPS.shrink(b10); FPS.shrink(b11)
    m.arr = [m.arr[2], m.arr[3], b10, b11]
    p[0], p[1] = p[1], rem

def inner_half_gcd(p: list) -> Mat:
    n = len(p[0]); m = len(p[1])
    k = n + 1 >> 1
    if m <= k: return Mat.I()
    m1 = inner_half_gcd([p[0][k:], p[1][k:]])
    p = m1 * p
    if len(p[1]) <= k: return m1
    inner_naive_gcd(m1, p)
    if len(p[1]) <= k: return m1
    l = len(p[0]) - 1
    j = 2 * k - l
    p[0] = p[0][j:]
    p[1] = p[1][j:]
    return inner_half_gcd(p) * m1

def inner_poly_gcd(a: list, b: list) -> Mat:
    p = [a[::], b[::]]
    FPS.shrink(p[0]); FPS.shrink(p[1])
    n = len(p[0]); m = len(p[1])
    if n < m:
        mat = inner_poly_gcd(p[1], p[0])
        mat.arr = [mat.arr[1], mat.arr[0], mat.arr[2], mat.arr[3]]
        return mat
    res = Mat.I()
    while 1:
        m1 = inner_half_gcd(p)
        p = m1 * p
        if not p[1]: return m1 * res
        inner_naive_gcd(m1, p)
        if not p[1]: return m1 * res
        res = m1 * res

def poly_gcd(a: list, b: list) -> list:
    p = [a, b]
    m = inner_poly_gcd(a, b)
    p = m * p
    if p[0]:
        coef = pow(p[0][-1], MOD - 2, MOD)
        for i, x in enumerate(p[0]): p[0][i] = x * coef % MOD
    return p[0]

def poly_inv(f: list, g: list) -> list:
    p = [f, g]
    m = inner_poly_gcd(f, g)
    gcd = (m * p)[0]
    if len(gcd) != 1: return [0, []]
    x = [[1], g]
    return [1, FPS.mul(FPS.mod((m * x)[0], g), pow(gcd[0], MOD - 2, MOD))]