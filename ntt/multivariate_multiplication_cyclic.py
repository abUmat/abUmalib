# my module
from mymath.primitive_root import *
from ntt.chirp_z import *
# my module
# https://judge.yosupo.jp/submission/136277
def multivariate_multiplication_cyclic(f: List[int], g: List[int], base: List[int], mod: int) -> List[int]:
    for n in base: assert((mod - 1) % n == 0)
    pr = primitive_root(mod)
    ipr = modinv(pr, mod)
    N = 1
    for n in base: N *= n
    assert(len(f) == N)
    assert(len(g) == N)
    root = [pow(pr, (mod - 1) // n, mod) for n in base]
    iroot = [pow(ipr, (mod - 1) // n, mod) for n in base]

    step = 1
    for i, n in enumerate(base):
        nxt = step * n
        for j in range(N):
            if j % nxt >= step: continue
            f[j:j + nxt:step] = chirp_z(f[j:j + nxt:step], root[i], n, 1, mod)
            g[j:j + nxt:step] = chirp_z(g[j:j + nxt:step], root[i], n, 1, mod)
        step = nxt

    for i, x in enumerate(g): f[i] = f[i] * x % mod

    step = 1
    for i, n in enumerate(base):
        nxt = step * n
        for j in range(N):
            if j % nxt >= step: continue
            f[j:j + nxt:step] = chirp_z(f[j:j + nxt:step], iroot[i], n, 1, mod)
        step = nxt

    cf = modinv(N, mod)
    return [x * cf % mod for x in f]