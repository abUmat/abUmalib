# my module
from fps.fps import *
# my module
# https://judge.yosupo.jp/submission/139183
def composition_inverse(f: Poly, mod: int, deg: int=-1) -> Poly:
    '''return: g s.t. f(g(x)) == g(f(x)) == x'''
    def composition_multi(Ps: List[Poly], Q: Poly, deg: int) -> Poly:
        k = int(deg ** .5+ 1)
        d = (deg + k) // k
        X = [[] for _ in range(k + 1)]
        X[0] = [1]
        for i, x in enumerate(X):
            if i == k: break
            X[i + 1] = fps.mul(x, Q)
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
                        y[t] += xx * P[i * d + j] % mod
                y = fps.mul(y, Z)
                y[deg + 1:] = []
                for j, yy in enumerate(y):
                    F[j] += yy
                Z = fps.mul(Z, xd)
                Z[deg + 1:] = []
            F.pop()
            ress.append([x % mod for x in F])
        return ress

    fps = FPS(mod)
    deg = len(f) if deg == -1 else deg
    dfdx = fps.diff(f)
    f = [-x for x in f]
    res = [0]
    m = 1
    while m < deg:
        m <<= 1
        cf0, cf1 = composition_multi([f, dfdx], res, m)
        cf0[1] += 1
        tmp = fps.mul(cf0, fps.inv(cf1, m))
        res[m >> 1:] = tmp[m >> 1:min(deg, m)]
    return res
