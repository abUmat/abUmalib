# my module
from math998244353.fps import *
# my module
def linear_recurrence(k: int, Q: list, P: list) -> int:
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

    dw = pow(pow(3, MOD - 2, MOD), (MOD - 1) // (N << 1), MOD)

    while k:
        inv2 = pow(2, MOD - 2, MOD)
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

def kitamasa(N: int, Q: list, a: list) -> int:
    if N < len(a): return a[N]
    P = NTT.multiply(a[:len(Q) - 1], Q)
    FPS.resize(P, len(Q) - 1)
    return linear_recurrence(N, Q, P)
