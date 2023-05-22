# my module
from math998244353.fps import *
# my module
# https://judge.yosupo.jp/submission/83016
def composition(P: list, Q: list, deg: int=-1) -> list:
    if deg == -1: deg = min(len(P), len(Q))
    k = int(deg ** .5+ 1)
    d = (deg + k) // k

    X = [[] for _ in range(k + 1)]
    X[0] = [1]
    for i, x in enumerate(X):
        if i == k: break
        X[i + 1] = NTT.multiply(x, Q)
        X[i + 1][deg + 1:] = []
    leny = len(X[-1])
    X[d + 1:] = []
    xd = X.pop()
    lenp = len(P)

    Z = [1]
    F = [0] * (deg + 1)
    for i in range(k):
        y = [0] * leny
        for j, x in enumerate(X):
            if i * d + j >= lenp: break
            for t, xx in enumerate(x):
                y[t] += xx * P[i * d + j] % MOD
        y = NTT.multiply(y, Z)
        y[deg + 1:] = []
        for j, yy in enumerate(y):
            F[j] += yy
        Z = NTT.multiply(Z, xd)
        Z[deg + 1:] = []
    F.pop()
    return [x % MOD for x in F]

def composition_multi(Ps: list, Q: list, deg: int) -> list:
    k = int(deg ** .5+ 1)
    d = (deg + k) // k

    X = [[] for _ in range(k + 1)]
    X[0] = [1]
    for i, x in enumerate(X):
        if i == k: break
        X[i + 1] = NTT.multiply(x, Q)
        X[i + 1][deg + 1:] = []
    leny = len(X[-1])
    X[d + 1:] = []
    xd = X.pop()

    ress = []
    for P in Ps:
        lenp = len(P)
        Z = [1]
        F = [0] * (deg + 1)
        for i in range(k):
            y = [0] * leny
            for j, x in enumerate(X):
                if i * d + j >= lenp: break
                for t, xx in enumerate(x):
                    y[t] += xx * P[i * d + j] % MOD
            y = NTT.multiply(y, Z)
            y[deg + 1:] = []
            for j, yy in enumerate(y):
                F[j] += yy
            Z = NTT.multiply(Z, xd)
            Z[deg + 1:] = []
        F.pop()
        ress.append([x % MOD for x in F])
    return ress
