# my module
from ntt.ntt import *
# my module
def multivariate_multiplication(f: List[int], g: List[int], base: List[int], mod: int) -> List[int]:
    n = len(f); s = len(base); W = 1
    if s == 0:
        return [f[0] * g[0] % mod]
    while W < n << 1: W <<= 1
    chi = [0] * n
    for i in range(n):
        x = i
        for j in range(s - 1):
            x //= base[j]
            chi[i] += x
        chi[i] %= s
    F = [[0] * W for _ in range(s)]
    G = [[0] * W for _ in range(s)]
    for i, (j, x, y) in enumerate(zip(chi, f, g)):
        F[j][i] = x
        G[j][i] = y
    ntt = NTT(mod)
    for i, (f, g) in enumerate(zip(F, G)): ntt.ntt(f); ntt.ntt(g)
    for k in range(W):
        a = [0] * s
        for i, f in enumerate(F):
            for j, g in enumerate(G):
                a[i + j - (s if i + j >= s else 0)] += f[k] * g[k] % mod
        for i, f in enumerate(F):
            f[k] = a[i] % mod
    for i, f in enumerate(F): ntt.intt(f)
    return [F[j][i] for i, j in enumerate(chi)]
