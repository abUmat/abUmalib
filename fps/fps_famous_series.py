# my module
from gcc_builtins import *
from fps.formal_power_series import *
from modulo.binominal import *
from fps.taylor_shift import *
# my module
def stirling1(N: int, C: Binominal) -> FormalPowerSeries:
    mod = C.mod
    if N <= 0:
        res = FormalPowerSeries([1]); res.mod = mod
        return res
    lg = 31 - clz(N)
    res = FormalPowerSeries([0, 1]); res.mod = mod
    for i in range(lg)[::-1]:
        n = N >> i
        res = res * taylor_shift(res, (n >> 1) % mod, C)
        if n & 1: res = (res << 1) + res * (n - 1)
    res.reduction()
    return res

def stirling2(N: int, C: Binominal) -> FormalPowerSeries:
    mod = C.mod
    f = FormalPowerSeries([pow(i, N, mod) * C.finv(i) % mod for i in range(N + 1)]); f.mod = mod
    g = FormalPowerSeries([-C.finv(i) if i & 1 else C.finv(i) for i in range(N + 1)]); g.mod = mod
    return (f * g)[:N + 1]

def bernoulli(N: int, C: Binominal) -> FormalPowerSeries:
    mod = C.mod
    res = FormalPowerSeries([C.finv(i + 1) for i in range(N + 1)]); res.mod = mod
    return res.inv(N + 1)

def partition(N: int, C: Binominal) -> FormalPowerSeries:
    mod = C.mod
    res = [0] * (N + 1)
    res[0] = 1
    for k in range(1, N + 1):
        k1 = k * (3 * k + 1) >> 1
        k2 = k * (3 * k - 1) >> 1
        if k2 > N: break
        if k1 <= N: res[k1] += (-1 if k & 1 else 1)
        if k2 <= N: res[k2] += (-1 if k & 1 else 1)
    res = FormalPowerSeries(res); res.mod = mod
    return res.inv()

def montmort(N: int, mod: int) -> List[int]:
    if N <= 1: return [0]
    if N == 2: return [0, 1]
    f = [0] * N
    f[0] = 0; f[1] = 1
    for i in range(2, N): f[i] = (f[i - 1] + f[i - 2]) * i % mod
    return f
