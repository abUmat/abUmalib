# my module
from misc.typing_template import *
from modulo.modinv import *
# my module
# https://nyaannyaan.github.io/library/matrix/characteristric-polynomial.hpp
def characteristic_polynomial(a: Matrix, mod: int) -> Vector:
    a = [ai[:] for ai in a]
    N = len(a)
    for j in range(N - 2):
        for i in range(j + 1, N):
            if a[i][j]:
                a[i], a[j + 1] = a[j + 1], a[i]
                for ak in a: ak[i], ak[j + 1] = ak[j + 1], ak[i]
                break
        if a[j + 1][j]:
            aj1 = a[j + 1]
            inv = modinv(aj1[j], mod)
            for i in range(j + 2, N):
                ai = a[i]
                if not ai[j]: continue
                coef = inv * ai[j] % mod
                ai[j] = 0
                for l in range(j + 1, N):
                    ai[l] -= coef * aj1[l]
                    ai[l] %= mod
                for ak in a:
                    ak[j + 1] += coef * ak[i]
                    ak[j + 1] %= mod

    p: List[Vector] = [[] for _ in range(N + 1)]
    p[0] = pim1 = [1]
    for i in range(1, N + 1):
        pi = [0] * (i + 1)
        for j in range(i):
            pi[j + 1] -= pim1[j]
            pi[j] += pim1[j] * a[i - 1][i - 1] % mod
        x = 1
        for m in range(1, i):
            x = x * (-a[i - m][i - m - 1]) % mod
            coef = x * a[i - m - 1][i - 1] % mod
            for j in range(i - m):
                pi[j] += coef * p[i - m - 1][j] % mod
        p[i] = pim1 = [x % mod for x in pi]
    return p[-1]
