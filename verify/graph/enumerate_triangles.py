# https://judge.yosupo.jp/problem/enumerate_triangles
# my module
from misc.fastio import *
from graph.enumerate_triangles import *
# my module
mod = 998244353
N, M = rd(), rd()
A = rdl(N)
edges = [0] * M
for i in range(M):
    u, v = rd(), rd()
    edges[i] = u << 20 | v
ans = 0
def func(i: int, j: int, k: int) -> None:
    global ans
    ans += (A[i] * A[j] % mod) * A[k] % mod
enumerate_triangles(N, edges, func)
wtn(ans % mod)