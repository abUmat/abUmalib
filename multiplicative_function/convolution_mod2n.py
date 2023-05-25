# my module
from ntt.ntt import *
# my module
# https://judge.yosupo.jp/submission/73323
def multiplicative_convolution_mod2n(A: list, B: list, mod: int) -> list:
    N = 0
    while 1 << N < len(A): N += 1
    assert(1 << N == len(A) and 1 << N == len(B))
    ntt = NTT(mod)

    mask = (1 << N) - 1

    AA = [[[]] for _ in range(N + 1)]
    BB = [[[]] for _ in range(N + 1)]
    CC = [[[]] for _ in range(N + 1)]

    def shape(n: int) -> tuple:
        H = 2 if N - n >= 2 else 1
        W = 1 << max(N - n - 2, 0)
        return H, W

    for n in range(N + 1):
        H, W = shape(n)
        AA[n] = [[0] * W for _ in range(H)]
        BB[n] = [[0] * W for _ in range(H)]
        CC[n] = [[0] * W for _ in range(H)]
        x = (1 << n) & mask
        a = AA[n]; b = BB[n]
        for j in range(W):
            a[0][j] = A[x]
            b[0][j] = B[x]
            if H == 2:
                a[1][j] = A[-x]
                b[1][j] = B[-x]
            x = (x * 5) & mask

    for n in range(N + 1):
        a = AA[n]; b = BB[n]
        H, W = shape(n)
        for i in range(H):
            ntt.ntt(a[i])
            ntt.ntt(b[i])
        if H == 2:
            for j in range(W):
                a[0][j], a[1][j] = a[0][j] + a[1][j], a[0][j] - a[1][j]
                b[0][j], b[1][j] = b[0][j] + b[1][j], b[0][j] - b[1][j]

    for n1 in range(N + 1):
        for n2 in range(N + 1):
            n3 = min(N, n1 + n2)
            H, W = shape(n3)
            for i in range(H):
                for j in range(W):
                    CC[n3][i][j] += AA[n1][i][j] * BB[n2][i][j] % mod

    for n in range(N + 1):
        c = CC[n]
        H, W = shape(n)
        for i in range(H): ntt.intt(c[i])
        if H == 2:
            for j in range(W):
                c[0][j], c[1][j] = c[0][j] + c[1][j], c[0][j] - c[1][j]
        coef = modinv(H, mod)
        for i in range(H):
            for j in range(W):
                c[i][j] = c[i][j] * coef % mod

    C = [0] * (1 << N)
    for n in range(N + 1):
        H, W = shape(n)
        x = (1 << n) & mask
        c = CC[n]
        for j in range(W):
            C[x] = c[0][j]
            if H == 2: C[(1 << N) - x] = c[1][j]
            x = (x * 5) & mask
    return C
