from math import log2
# my module
from modulo.binomial import *
from math998244353.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/fps-composition.hpp
def composition(P: list, Q: list, C: Binomial, deg: int=-1) -> list:
    N = min(len(P), len(Q)) if deg == -1 else deg
    if not N: return []
    FPS.shrink(P)
    if not P:
        R = [0] * N
        R[0] = Q[0] if Q else 0
        return R
    if N == 1: return FPS.eval(Q, P[0])

    P[N:] = []; P[len(P):] = [0] * (N - len(P))
    Q[N:] = []; Q[len(Q):] = [0] * (N - len(Q))
    M = int(max(1, (N / log2(N)) ** 0.5))
    L = (N + M - 1) // M
    Pm = P[:M]
    Pr = P[M:]

    J = (N - 1).bit_length()
    pms = [[] for _ in range(J)]
    pms[0] = Pm
    for i in range(1, J): pms[i] = NTT.pow2(pms[i - 1])[:N]

    def comp(left: int, j: int) -> list:
        if j == 1:
            Q1 = Q[left + 0] if left + 0 < len(Q) else 0
            Q2 = Q[left + 1] if left + 1 < len(Q) else 0
            return FPS.add(FPS.mul(pms[0][:N], Q2), Q1)
        if N <= left: return []
        Q1 = comp(left, j - 1)
        Q2 = comp(left + (1 << (j - 1)), j - 1)
        return FPS.add(Q1, NTT.multiply(pms[j - 1][:N], Q2))[:N]

    QPm = comp(0, J)
    R = QPm[:]
    pw_Pr = [1]
    dPm = FPS.diff(Pm)
    FPS.shrink(dPm)
    deg_dPm = 0
    while deg_dPm != len(dPm) and dPm[deg_dPm] == 0: deg_dPm += 1
    idPm = FPS.inv(dPm[deg_dPm:], N) if dPm else []

    d = M
    for l in range(1, L + 1):
        if d >= N: break
        pw_Pr = NTT.multiply(pw_Pr, Pr)[:N - d]
        if dPm:
            idPm[N - d:] = []; idPm[len(idPm):] = [0] * (N - d - len(idPm))
            QPm = NTT.multiply(FPS.diff(QPm)[deg_dPm:], idPm)[:N - d]
            tmp = FPS.mul(NTT.multiply(QPm, pw_Pr)[:N - d], C.finv(l))
        else:
            tmp = FPS.mul(pw_Pr, Q[l])
        tmp[:0] = [0] * d
        R = FPS.add(R, tmp)
        d += M
    R[N:] = []; R[len(R):] = [0] * (N - len(R))
    return R
