# my module
from fps.berlekamp_massey import *
from fps.fps import *
from fps.mod_pow import *
# my module
from random import randint
from copy import deepcopy
# https://nyaannyaan.github.io/library/matrix/black-box-linear-algebra.hpp
def inner_product(a: Poly, b: Poly, mod: int) -> int:
    res = 0
    n = len(a)
    assert(n == len(b))
    for i in range(n): res += a[i] * b[i] % mod
    return res % mod

def random_poly(n: int, mod: int) -> Poly:
    return [randint(0, mod - 1) for _ in range(n)]

class ModMatrix:
    def __init__(self, n: int, mod: int) -> None:
        self.mat = [[0] * n for _ in range(n)]
        self.mod = mod

    def add(self, i: int, j: int, x: int) -> None:
        self.mat[i][j] += x

    def __mul__(self, r: Poly) -> Poly:
        assert(len(self.mat) == len(r))
        mod = self.mod
        return [sum(matij * r[j] % mod for j, matij in enumerate(mati)) % mod for mati in self.mat]

    def apply(self, i: int, r: int) -> None:
        mod = self.mod
        for j, matij in enumerate(self.mat[i]):
            self.mat[i][j] = matij * r % mod

class SparseMatrix:
    def __init__(self, n: int, mod: int) -> None:
        self.mat: List[List[int]] = [[] for _ in range(n)]
        self.mod = mod

    def add(self, i: int, j: int, x: int) -> None:
        self.mat[i].append(j << 30 | x)

    def __mul__(self, r: Poly) -> Poly:
        assert(len(self.mat) == len(r))
        mod = self.mod
        return [sum((jx & 0x3fffffff) * r[jx >> 30] % mod for jx in mati) % mod for mati in self.mat]

    def apply(self, i: int, r: int) -> None:
        mod = self.mod
        for idx, jx in enumerate(self.mat[i]):
            self.mat[i][idx] = (jx >> 30) << 30 | ((jx & 0x3fffffff) * r % mod)

def vector_minpoly(b: List[Poly], mod: int) -> Poly:
    assert(b)
    n = len(b); m = len(b[0])
    u = random_poly(m, mod)
    a = [0] * n
    for i, bi in enumerate(b): a[i] = inner_product(bi, u, mod)
    return berlekamp_massey(a, mod)

def mat_minpoly(A: Union[ModMatrix, SparseMatrix]) -> Poly:
    n = len(A.mat)
    u = random_poly(n, A.mod)
    b: List[Poly] = [0] * (n << 1 | 1)
    for i in range(len(b)):
        b[i] = u
        u = A * u
    return vector_minpoly(b, A.mod)

def fast_pow(A: Union[ModMatrix, SparseMatrix], b: Poly, k: int) -> Poly:
    n = len(b)
    mp = mat_minpoly(A)
    fps = FPS(A.mod)
    c = mod_pow(k, [0, 1], mp[::-1], A.mod, fps)
    res = [0] * n
    for ci in c:
        res = fps.add(res, fps.mul(b, ci))
        b = A * b
    return res

def fast_det(A: Union[ModMatrix, SparseMatrix]) -> int:
    n = len(A.mat)
    assert(n == len(A.mat))
    mod = A.mod
    D = random_poly(n, mod)
    while 1:
        while any([not x for x in D]): D = random_poly(n, mod)
        AD = deepcopy(A)
        for i, d in enumerate(D): AD.apply(i, d)
        mp = mat_minpoly(AD)
        if mp[-1] == 0: return 0
        if len(mp) != n + 1: continue
        det = -mp[-1] if n & 1 else mp[-1]
        Ddet = 1
        for d in D: Ddet = Ddet * d % mod
        return det * modinv(Ddet, mod) % mod
    exit(1)
