from math import log2
# my module
from fps.fps import *
from modulo.binomial import *
# my module
# https://nyaannyaan.github.io/library/fps/fps-composition.hpp
def composition(P: list, Q: list, C: Binomial, deg: int=-1) -> list:
    mod = C.mod
    N = min(len(P), len(Q)) if deg == -1 else deg
    if not N: return []
    FPS.shrink(P)
    if not P:
        R = [0] * N
        R[0] = Q[0] if Q else 0
        return R
    if N == 1: return FPS(mod).eval(Q, P[0])

    FPS.resize(P, N); FPS.resize(Q, N)
    M = int(max(1, (N / log2(N)) ** 0.5))
    L = (N + M - 1) // M
    Pm = P[:M]
    Pr = P[M:]

    fps = FPS(mod)
    J = (N - 1).bit_length()
    pms = [[] for _ in range(J)]
    pms[0] = Pm
    for i in range(1, J): pms[i] = fps.mul(pms[i - 1][:N], pms[i - 1][:N])

    def comp(left: int, j: int) -> list:
        if j == 1:
            Q1 = Q[left + 0] if left + 0 < len(Q) else 0
            Q2 = Q[left + 1] if left + 1 < len(Q) else 0
            return fps.add(fps.mul(pms[0][:N], Q2), Q1)
        if N <= left: return []
        Q1 = comp(left, j - 1)
        Q2 = comp(left + (1 << (j - 1)), j - 1)
        return fps.add(Q1, fps.mul(pms[j - 1][:N], Q2))[:N]

    QPm = comp(0, J)
    R = QPm[:]
    pw_Pr = [1]
    dPm = fps.diff(Pm)
    FPS.shrink(dPm)
    deg_dPm = 0
    while deg_dPm != len(dPm) and dPm[deg_dPm] == 0: deg_dPm += 1
    idPm = fps.inv(dPm[deg_dPm:], N) if dPm else []

    d = M
    for l in range(1, L + 1):
        if d >= N: break
        pw_Pr = fps.mul(pw_Pr, Pr)[:N - d]
        if dPm:
            idPm[N - d:] = []
            QPm = fps.mul(fps.diff(QPm)[deg_dPm:], idPm)[:N - d]
            tmp = fps.mul(fps.mul(QPm, pw_Pr)[:N - d], C.finv(l))
        else:
            tmp = fps.mul(pw_Pr, Q[l])
        tmp[:0] = [0] * d
        R = fps.add(R, tmp)
        d += M
    FPS.resize(R, N)
    return R
