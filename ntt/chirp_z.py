# my module
from ntt.arbitrary_ntt import *
# my module
def chirp_z(mod: int, f: list, W: int, N: int=-1, A: int=1) -> list:
    if N == -1: N = len(f)
    if not f or N == 0: return []
    M = len(f)
    if A != -1:
        x = 1
        for i in range(M):
            f[i] = f[i] * x % mod
            x = x * A % mod
    if W == 0:
        F = [f[0]] * N
        F[0] = sum(f) % mod
        return F
    wc = [0] * (N + M)
    iwc = [0] * max(N, M)
    ws = 1; iW = pow(W, mod - 2, mod); iws = 1
    wc[0] = iwc[0] = 1
    tmp = 1
    for i in range(1, N + M):
        wc[i] = tmp = ws * tmp % mod
        ws = ws * W % mod
    tmp = 1
    for i in range(1, max(N, M)):
        iwc[i] = tmp = iws * tmp % mod
        iws = iws * iW % mod
    for i, x in enumerate(f): f[i] = x * iwc[i] % mod
    f.reverse()
    g = ArbitraryNTT.multiply(f, wc, mod)
    F = [0] * N
    for i, x in enumerate(iwc):
        if i == N: break
        F[i] = g[M - 1 + i] * x % mod
    return F
