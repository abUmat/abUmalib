# my module
from math998244353.ntt import *
# my module
# https://nyaannyaan.github.io/library/ntt/chirp-z.hpp
# abst. https://yoneh.hatenadiary.org/entry/20080109/1199862684
def chirp_z(f: Poly, W: int, N: int=-1, A: int=1) -> Poly:
    if N == -1: N = len(f)
    if not f or N == 0: return []
    M = len(f)
    if A != -1:
        x = 1
        for i in range(M):
            f[i] = f[i] * x % MOD
            x = x * A % MOD
    if W == 0:
        F = [f[0]] * N
        F[0] = sum(f) % MOD
        return F
    wc = [0] * (N + M)
    iwc = [0] * max(N, M)
    ws = 1; iW = modinv(W, MOD); iws = 1
    wc[0] = iwc[0] = 1
    tmp = 1
    for i in range(1, N + M):
        wc[i] = tmp = ws * tmp % MOD
        ws = ws * W % MOD
    tmp = 1
    for i in range(1, max(N, M)):
        iwc[i] = tmp = iws * tmp % MOD
        iws = iws * iW % MOD
    for i, x in enumerate(f): f[i] = x * iwc[i] % MOD
    f.reverse()
    g = NTT.multiply(f, wc)
    F = [0] * N
    for i, x in enumerate(iwc):
        if i == N: break
        F[i] = g[M - 1 + i] * x % MOD
    return F