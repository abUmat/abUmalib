# my module
from matrix.gauss_elimination import *
# my module
# https://nyaannyaan.github.io/library/matrix/inverse-matrix.hpp
def inverse_matrix(a: Matrix, mod: int) -> Matrix:
    N = len(a)
    assert(N)
    assert(N == len(a[0]))
    m = [ai + [0] * N for ai in a]
    for i, mi in enumerate(m): mi[N + i] = 1
    rank, _ = gauss_elimination(m, mod, N, True)
    if rank != N: return []
    return [mi[N:] for mi in m]
