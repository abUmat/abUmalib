# my module
from math998244353.ntt import *
# my module
# https://nyaannyaan.github.io/library/ntt/multivariate-multiplication.hpp
def multivariate_multiplication(f: list, g: list, base: list) -> list:
    n = len(f); s = len(base); W = 1
    if s == 0: return [f[0] * g[0] % MOD]
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
    for i, j in enumerate(chi):
        F[j][i] = f[i]
        G[j][i] = g[i]
    for i in range(s): NTT.ntt(F[i]); NTT.ntt(G[i])
    for k in range(W):
        a = [0] * s
        for i, f in enumerate(F):
            tmp = f[k]
            for j, g in enumerate(G):
                a[i + j - (s if i + j >= s else 0)] += tmp * g[k] % MOD
        for i, f in enumerate(F):
            f[k] = a[i] % MOD
    for f in F: NTT.intt(f)
    return [F[j][i] for i, j in enumerate(chi)]