# my module
from fps.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/polynomial-gcd.hpp
class Mat:
    def __init__(self, a00: Poly, a01: Poly, a10: Poly, a11: Poly) -> None:
        self.arr = [a00, a01, a10, a11]

    @staticmethod
    def mul(l, r, fps: FPS) -> List[Poly]:
        a00, a01, a10, a11 = l.arr
        if type(r) is Mat:
            ra00, ra01, ra10, ra11 = r.arr
            A00 = fps.add(fps.mul(a00, ra00), fps.mul(a01, ra10))
            A01 = fps.add(fps.mul(a00, ra01), fps.mul(a01, ra11))
            A10 = fps.add(fps.mul(a10, ra00), fps.mul(a11, ra10))
            A11 = fps.add(fps.mul(a10, ra01), fps.mul(a11, ra11))
            FPS.shrink(A00); FPS.shrink(A01); FPS.shrink(A10); FPS.shrink(A11)
            return Mat(A00, A01, A10, A11)
        b0 = fps.add(fps.mul(a00, r[0]), fps.mul(a01, r[1]))
        b1 = fps.add(fps.mul(a10, r[0]), fps.mul(a11, r[1]))
        FPS.shrink(b0); FPS.shrink(b1)
        return [b0, b1]

    @staticmethod
    def I():
        return Mat([1], [], [], [1])

def inner_naive_gcd(m: Mat, p: List[Poly], fps: FPS) -> None:
    quo, rem = fps.divmod(p[0], p[1])
    b10 = fps.sub(m.arr[0], fps.mul(m.arr[2], quo))
    b11 = fps.sub(m.arr[1], fps.mul(m.arr[3], quo))
    FPS.shrink(rem); FPS.shrink(b10); FPS.shrink(b11)
    m.arr = [m.arr[2], m.arr[3], b10, b11]
    p[0], p[1] = p[1], rem

def inner_half_gcd(p: List[Poly], fps: FPS) -> Mat:
    n = len(p[0]); m = len(p[1])
    k = n + 1 >> 1
    if m <= k: return Mat.I()
    m1 = inner_half_gcd([p[0][k:], p[1][k:]], fps)
    p = Mat.mul(m1, p, fps)
    if len(p[1]) <= k: return m1
    inner_naive_gcd(m1, p, fps)
    if len(p[1]) <= k: return m1
    l = len(p[0]) - 1
    j = 2 * k - l
    p[0] = p[0][j:]
    p[1] = p[1][j:]
    return Mat.mul(inner_half_gcd(p, fps), m1, fps)

def inner_poly_gcd(a: Poly, b: Poly, mod: int) -> Mat:
    p = [a[::], b[::]]
    FPS.shrink(p[0]); FPS.shrink(p[1])
    n = len(p[0]); m = len(p[1])
    if n < m:
        mat = inner_poly_gcd(p[1], p[0], mod)
        mat.arr = [mat.arr[1], mat.arr[0], mat.arr[2], mat.arr[3]]
        return mat
    res = Mat.I()
    fps = FPS(mod)
    while 1:
        m1 = inner_half_gcd(p, fps)
        p = Mat.mul(m1, p, fps)
        if not p[1]: return Mat.mul(m1, res, fps)
        inner_naive_gcd(m1, p, fps)
        if not p[1]: return Mat.mul(m1, res, fps)
        res = Mat.mul(m1, res, fps)

def poly_gcd(a: Poly, b: Poly, mod: int) -> Poly:
    fps = FPS(mod)
    p = [a, b]
    m = inner_poly_gcd(a, b, mod)
    p = Mat.mul(m, p, fps)
    if p[0]:
        coef = modinv(p[0][-1], mod)
        p[0] = fps.mul(p[0], coef)
    return p[0]

def poly_inv(f: Poly, g: Poly, mod: int) -> Poly:
    '''return: h s.t. f*h == 1 (mod g)'''
    fps = FPS(mod)
    p = [f, g]
    m = inner_poly_gcd(f, g, mod)
    gcd = Mat.mul(m, p, fps)[0]
    if len(gcd) != 1: return [0, []]
    x = [[1], g]
    return [1, fps.mul(fps.modulo(Mat.mul(m, x, fps)[0], g), modinv(gcd[0], mod))]
