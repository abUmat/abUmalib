# my module
from misc.typing_template import *
from modulo.modinv import *
# my module
# https://nyaannyaan.github.io/library/matrix/gauss-elimination.hpp
def gauss_elimination(a: Matrix, mod: int, pivot_end: int=-1, diagonalize: bool=False) -> Tuple[int, int]:
    H = len(a); W = len(a[0]); rank = 0
    if pivot_end == -1: pivot_end = W
    det = 1
    for j in range(pivot_end):
        for i in range(rank, H):
            if a[i][j]: break
        else:
            det = 0
            continue
        if rank != i:
            det = -det
            a[rank], a[i] = a[i], a[rank]
        ar = a[rank]
        arj = ar[j]
        inv_arj = modinv(arj, mod)
        det *= arj
        det %= mod
        if diagonalize and arj != 1:
            ar[j] = 1
            for k in range(j + 1, W):
                ar[k] *= inv_arj
                ar[k] %= mod
            inv_arj = 1
        is_ = 0 if diagonalize else rank + 1
        for i in range(is_, H):
            if i == rank: continue
            ai = a[i]
            if ai[j]:
                coef = ai[j] * inv_arj % mod
                ai[j] = 0
                for k in range(j + 1, W):
                    ai[k] -= ar[k] * coef
                    ai[k] %= mod
        rank += 1
    return rank, det
