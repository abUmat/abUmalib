# my module
from math998244353.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/kitamasa.hpp
def linear_recurrence(k: int, Q: Poly, P: Poly) -> int:
    '''return: [x**k](P/Q)'''
    FPS.shrink(Q)
    ret = 0
    if len(P) >= len(Q):
        R, P = FPS.divmod(P, Q)
        FPS.shrink(P)
        if k < len(R): ret += R[k]
    if len(P) == 0: return ret

    N = 1
    while N < len(Q): N <<= 1

    FPS.resize(P, N << 1)
    FPS.resize(Q, N << 1)
    NTT.ntt(P)
    NTT.ntt(Q)
    S = [0] * (N << 1)
    T = [0] * (N << 1)
    btr = [0] * N
    logn = (N & -N).bit_length() - 1
    for i in range(1 << logn):
        btr[i] = (btr[i >> 1] >> 1) + ((i & 1) << (logn - 1))

    dw = pow(332748118, (MOD - 1) // (N << 1), MOD) # 332748118 * 3 == 1 (mod 998244353)

    while k:
        inv2 = 499122177 # 499122177 * 2 == 1 (mod 998244353)
        FPS.resize(T, N)
        for i in range(N):
            T[i] = Q[i << 1 | 0] * Q[i << 1 | 1] % MOD
        FPS.resize(S, N)
        if k & 1:
            for i in btr:
                S[i] = (P[i << 1 | 0] * Q[i << 1 | 1] - P[i << 1 | 1] * Q[i << 1 | 0]) % MOD * inv2 % MOD
                inv2 = inv2 * dw % MOD
        else:
            for i in range(N):
                S[i] = (P[i << 1 | 0] * Q[i << 1 | 1] + P[i << 1 | 1] * Q[i << 1 | 0]) % MOD * inv2 % MOD

        P, S = S, P
        Q, T = T, Q
        k >>= 1
        if k < N: break
        NTT.ntt_doubling(P)
        NTT.ntt_doubling(Q)
    NTT.intt(P)
    NTT.intt(Q)
    return ret + NTT.multiply(P, FPS.inv(Q))[k]

def kitamasa(N: int, Q: Poly, a: Poly) -> int:
    if N < len(a): return a[N]
    P = NTT.multiply(a[:len(Q) - 1], Q)
    FPS.resize(P, len(Q) - 1)
    return linear_recurrence(N, Q, P)
