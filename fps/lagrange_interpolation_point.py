# my module
from modulo.binomial import *
# my module
def lagrange_interpolation(y: list, x: int, C: Binomial, mod: int) -> int:
    N = len(y) - 1
    if x <= N: return y[x] % mod
    res = 0
    dp = [1] * (N + 1)
    x %= mod
    tmp = 1
    for i in range(N):
        dp[i + 1] = tmp = tmp * x % mod
        x -= 1
    pd = [1] * (N + 1)
    tmp = 1
    for i in range(N, 0, -1):
        pd[i - 1] = tmp = tmp * x % mod
        x += 1
    for i in range(N + 1):
        tmp = (((y[i] * dp[i] % mod) * pd[i] % mod) * C.finv(i) % mod) * C.finv(N - i) % mod
        res += -tmp if (N - i) & 1 else tmp
    return res % mod
