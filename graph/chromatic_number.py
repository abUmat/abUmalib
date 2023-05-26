# my module
from gcc_builtins import *
# my module
# https://nyaannyaan.github.io/library/graph/chromatic-number.hpp
def _calc(n: int, _hist, mod: int) -> int:
    hist = _hist[::]
    for c in range(1, n + 1):
        sm = 0
        for i, (j, x) in enumerate(hist):
            x = x * j % mod
            sm += x
            hist[i] = j, x
        if sm % mod: return c
    return n

def chromatic_number(g):
    n = len(g)
    adj = [0] * n
    dp = [0] * (1 << n)
    for i in range(n):
        for j in g[i]:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    dp[0] = 1
    for i in range(1, 1 << n):
        j = ctz(i)
        k = i & (i - 1)
        dp[i] = dp[k] + dp[k & ~adj[j]]
    memo = [0] * ((1 << n) + 1)
    for i in range(1 << n): memo[dp[i]] += -1 if parity(i) else 1
    hist = [[i, memo[i]] for i in range(1, (1 << n) + 1) if memo[i]]
    return min(_calc(n, hist, 1000000021), _calc(n, hist, 1000000033))