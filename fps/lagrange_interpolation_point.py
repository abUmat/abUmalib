# my module
from modulo.binomial import *
from misc.typing_template import *
# my module
# https://nyaannyaan.github.io/library/fps/lagrange-interpolation-point.hpp
def lagrange_interpolation(y: Vector, x: int, C: Binomial) -> int:
    '''
    y: f(0), f(1)....f(k)
    return: f(x)
    '''
    mod = C.mod
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
