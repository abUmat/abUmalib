# my module
from fps.formal_power_series import *
from modulo.binomial import *
# my module
def taylor_shift(f: FormalPowerSeries, a: int, C: Binomial):
    mod = f.mod
    N = len(f)
    res = [f[i] * C.fac(i) % mod for i in range(N)]
    res.reverse()
    g = [0] * N
    g[0] = 1
    for i in range(1, N): g[i] = (g[i - 1] * a % mod) * C.inv(i) % mod
    res = FormalPowerSeries(res); res.mod = mod
    res = (res * FormalPowerSeries(g))[:N]
    res.reverse()
    for i in range(N): res[i] = res[i] * C.finv(i) % mod
    return res
