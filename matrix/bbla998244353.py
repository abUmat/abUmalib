# my module
from fps.berlekamp_massey import *
from math998244353.fps import *
from math998244353.mod_pow import *
# my module
from random import randint
from copy import deepcopy
# https://nyaannyaan.github.io/library/matrix/black-box-linear-algebra.hpp
def inner_product(a: Poly, b: Poly) -> int:
    res = 0
    n = len(a)
    assert(n == len(b))
    for i in range(n): res += a[i] * b[i] % MOD
    return res % MOD

def random_poly(n: int) -> Poly:
    return [randint(0, MOD - 1) for _ in range(n)]

class ModMatrix:
    def __init__(self, n: int) -> None:
        self.mat = [[0] * n for _ in range(n)]

    def add(self, i: int, j: int, x: int) -> None:
        self.mat[i][j] += x

    def __mul__(self, r: Poly) -> Poly:
        assert(len(self.mat) == len(r))
        return [sum(matij * r[j] % MOD for j, matij in enumerate(mati)) % MOD for mati in self.mat]

    def apply(self, i: int, r: int) -> None:
        for j, matij in enumerate(self.mat[i]):
            self.mat[i][j] = matij * r % MOD

class SparseMatrix:
    def __init__(self, n: int) -> None:
        self.mat: List[List[int]] = [[] for _ in range(n)]

    def add(self, i: int, j: int, x: int) -> None:
        self.mat[i].append(j << 30 | x)

    def __mul__(self, r: Poly) -> Poly:
        assert(len(self.mat) == len(r))
        return [sum((jx & 0x3fffffff) * r[jx >> 30] % MOD for jx in mati) % MOD for mati in self.mat]

    def apply(self, i: int, r: int) -> None:
        for idx, jx in enumerate(self.mat[i]):
            self.mat[i][idx] = (jx >> 30) << 30 | ((jx & 0x3fffffff) * r % MOD)

def vector_minpoly(b: List[Poly]) -> Poly:
    assert(b)
    n = len(b); m = len(b[0])
    u = random_poly(m)
    a = [0] * n
    for i, bi in enumerate(b): a[i] = inner_product(bi, u)
    return berlekamp_massey(a, MOD)

def mat_minpoly(A: Union[ModMatrix, SparseMatrix]) -> Poly:
    n = len(A.mat)
    u = random_poly(n)
    b: List[Poly] = [0] * (n << 1 | 1)
    for i in range(len(b)):
        b[i] = u
        u = A * u
    return vector_minpoly(b)

def fast_pow(A: Union[ModMatrix, SparseMatrix], b: Poly, k: int) -> Poly:
    n = len(b)
    mp = mat_minpoly(A)
    c = mod_pow(k, [0, 1], mp[::-1])
    res = [0] * n
    for ci in c:
        res = FPS.add(res, FPS.mul(b, ci))
        b = A * b
    return res

def fast_det(A: Union[ModMatrix, SparseMatrix]) -> int:
    n = len(A.mat)
    assert(n == len(A.mat))
    D = random_poly(n)
    while 1:
        while any([not x for x in D]): D = random_poly(n)
        AD = deepcopy(A)
        for i, d in enumerate(D): AD.apply(i, d)
        mp = mat_minpoly(AD)
        if mp[-1] == 0: return 0
        if len(mp) != n + 1: continue
        det = -mp[-1] if n & 1 else mp[-1]
        Ddet = 1
        for d in D: Ddet = Ddet * d % MOD
        return det * modinv(Ddet, MOD) % MOD
    exit(1)
