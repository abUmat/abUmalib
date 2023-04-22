# my module
from fps.formal_power_series import *
from modulo.mod_sqrt import *
# my module
def sqrt(f: FormalPowerSeries, deg: int=-1) -> FormalPowerSeries:
    mod = f.mod
    if deg == -1: deg = len(f)
    if len(f) == 0:
        ret = FormalPowerSeries([0] * deg); ret.mod = mod
        return ret
    if f[0] == 0:
        for i in range(1, len(f)):
            if f[i] != 0:
                if i & 1:
                    ret = FormalPowerSeries(); ret.mod = mod
                    return ret
                if deg - i // 2 <= 0: break
                ret = sqrt(f[i:], deg - i // 2)
                if not ret:
                    ret = FormalPowerSeries(); ret.mod = mod
                    return ret
                ret <<= i // 2
                if len(ret) < deg: ret = ret.resized(deg)
                return ret
        ret = FormalPowerSeries([0] * deg); ret.mod = mod
        return ret
    sqr = mod_sqrt(f[0], mod)
    if sqr == -1:
        ret = FormalPowerSeries(); ret.mod = mod
        return ret
    ret = FormalPowerSeries([sqr]); ret.mod = mod
    inv2 = pow(2, mod - 2, mod)
    i = 1
    while i < deg:
        ret = (ret + f[:i << 1] * ret.inv(i << 1)) * inv2
        i <<= 1
    return ret[:deg]
