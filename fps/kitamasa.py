# my module
from fps.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/kitamasa.hpp
def linear_recurrence(k: int, Q: Poly, P: Poly, mod: int) -> int:
    '''return: [x**k](P/Q)'''
    fps = FPS(mod)
    FPS.shrink(Q)
    ret = 0
    if len(P) >= len(Q):
        R, P = fps.divmod(P, Q)
        FPS.shrink(P)
        if k < len(R): ret += R[k]
    if len(P) == 0: return ret

    N = 1
    while N < len(Q): N <<= 1

    if fps.ntt is None:
        fps.resize(P, len(Q) - 1)
        while k:
            Q2 = Q[::]
            for i in range(1, len(Q2), 2): Q2[i] = -Q2[i]
            S = fps.mul(P, Q2)
            T = fps.mul(Q, Q2)
            if k & 1:
                for i in range(1, len(S), 2): P[i >> 1] = S[i]
                for i in range(0, len(T), 2): Q[i >> 1] = T[i]
            else:
                for i in range(0, len(S), 2): P[i >> 1] = S[i]
                for i in range(0, len(T), 2): Q[i >> 1] = T[i]
            k >>= 1
        return ret + P[0]
    ntt = fps.ntt.ntt
    intt = fps.ntt.intt
    ntt_doubling = fps.ntt.ntt_doubling
    FPS.resize(P, N << 1)
    FPS.resize(Q, N << 1)
    ntt(P)
    ntt(Q)
    S = [0] * (N << 1)
    T = [0] * (N << 1)
    btr = [0] * N
    logn = (N & -N).bit_length() - 1
    for i in range(1 << logn):
        btr[i] = (btr[i >> 1] >> 1) + ((i & 1) << (logn - 1))

    dw = pow(pow(3, mod - 2, mod), (mod - 1) // (N << 1), mod)

    while k:
        inv2 = pow(2, mod - 2, mod)
        FPS.resize(T, N)
        for i in range(N):
            T[i] = Q[i << 1 | 0] * Q[i << 1 | 1] % mod
        FPS.resize(S, N)
        if k & 1:
            for i in btr:
                S[i] = (P[i << 1 | 0] * Q[i << 1 | 1] - P[i << 1 | 1] * Q[i << 1 | 0]) % mod * inv2 % mod
                inv2 = inv2 * dw % mod
        else:
            for i in range(N):
                S[i] = (P[i << 1 | 0] * Q[i << 1 | 1] + P[i << 1 | 1] * Q[i << 1 | 0]) % mod * inv2 % mod

        P, S = S, P
        Q, T = T, Q
        k >>= 1
        if k < N: break
        ntt_doubling(P)
        ntt_doubling(Q)
    intt(P)
    intt(Q)
    return ret + fps.mul(P, fps.inv(Q))[k]

def kitamasa(N: int, Q: Poly, a: Poly, mod: int) -> int:
    if N < len(a): return a[N]
    P = FPS(mod).mul(a[:len(Q) - 1], Q)
    FPS.resize(P, len(Q) - 1)
    return linear_recurrence(N, Q, P, mod)
