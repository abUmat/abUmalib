# my module
from ntt.arbitrary_ntt import *
from fps.formal_power_series import *
# my module
def chirp_z(f: FormalPowerSeries, W: int, N: int=-1, A: int=1) -> FormalPowerSeries:
    mod = f.mod
    if N == -1: N = len(f)
    if not f or N == 0:
        res = FormalPowerSeries([]); res.mod = mod
        return res
    M = len(f)
    if A != -1:
        x = 1
        for i in range(M):
            f[i] = f[i] * x % mod
            x = x * A % mod
    if W == 0:
        F = [f[0]] * N
        for i in range(1, M): F[0] += f[i]
        F[0] %= mod
        F = FormalPowerSeries(F); F.mod = mod
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
    f = [x * y % mod for x, y in zip(f, iwc)]
    f.reverse()
    ntt = NTT(mod)
    g = ntt.multiply(f, wc)
    F = [x * y % mod for x, y in zip(g[M - 1: M + N - 1], iwc)]
    F = FormalPowerSeries(F); F.mod = mod
    return F
