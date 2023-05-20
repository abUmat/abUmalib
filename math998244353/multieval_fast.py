# my module
from math998244353.fps import *
# my module
# https://nyaannyaan.github.io/library/fps/fast-multieval.hpp
def multipoint_evaluation_fast(f: list, xs: list) -> list:
    s = len(xs)
    N = 1 << (s - 1).bit_length() if s != 1 else 2
    if not f or not xs: return [0] * s
    buf = [[] for _ in range(N << 1)]
    for i in range(N):
        n = -xs[i] if i < s else 0
        buf[i + N] = [n + 1, n - 1]
    for i in range(N - 1, 0, -1):
        g = buf[i << 1 | 0]
        h = buf[i << 1 | 1]
        n = len(g)
        m = n << 1
        FPS.resize(buf[i], n)
        for j in range(n):
            buf[i][j] = g[j] * h[j] % MOD - 1
        if i != 1:
            NTT.ntt_doubling(buf[i])
            buf[i][len(buf[i]):] = [0] * (m - len(buf[i]))
            for j in range(m):
                buf[i][j] += 1 if j < n else -1
    fs = len(f)
    root = buf[1]
    NTT.intt(root)
    root.append(1)
    root.reverse()
    tmp = FPS.inv(root, fs)
    tmp.reverse()
    root = NTT.multiply(tmp, f)
    root[:fs - 1] = []
    FPS.resize(root, N)

    ans = [0] * s

    def calc(i: int, l: int, r: int, g: list) -> None:
        if i >= N:
            ans[i - N] = g[0]
            return
        length = len(g)
        m = l + r >> 1
        NTT.ntt(g)
        tmp = buf[i << 1 | 1]
        for j in range(length): tmp[j] = tmp[j] * g[j] % MOD
        NTT.intt(tmp)
        calc(i << 1, l, m, tmp[length >> 1:])
        if m >= s: return
        tmp = buf[i << 1 | 0]
        for j in range(length): tmp[j] = tmp[j] * g[j] % MOD
        NTT.intt(tmp)
        calc(i << 1 | 1, m, r, tmp[length >> 1:])
    calc(1, 0, N, root)
    return ans