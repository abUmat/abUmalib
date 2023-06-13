# my module
from matrix.gauss_elimination import *
# my module
# https://nyaannyaan.github.io/library/matrix/linear-equation.hpp
def linear_equation(a: Matrix, b: Vector, mod: int) -> Matrix:
    a = [ai[:] for ai in a]
    H = len(a); W = len(a[0])
    for i, bi in enumerate(b): a[i].append(bi)
    rank, _ = gauss_elimination(a, mod, W, True)
    for i in range(rank, H):
        if a[i][-1]: return []
    res: Matrix = [[0] * W]
    pivot = [-1] * W
    j = 0
    for i, ai in enumerate(a):
        if i == rank: break
        for j in range(j, W + 1):
            if ai[j]: break
        res[0][j] = ai[-1]
        pivot[j] = i
    for j, pj in enumerate(pivot):
        if pj == -1:
            x = [0] * W
            x[j] = 1
            for k, pk in enumerate(pivot):
                if k == j: break
                if pk != -1:
                    x[k] = mod - a[pk][j] if a[pk][j] else 0
            res.append(x)
    return res
