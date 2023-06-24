# https://judge.yosupo.jp/problem/enumerate_cliques
# my module
from misc.fastio import *
from graph.enumerate_cliques import *
# my module
mod = 998244353
N, M = rd(), rd()
A = rdl(N)
edges = [0] * M
for i in range(M):
    u, v = rd(), rd()
    edges[i] = u << 20 | v
ans = 0
def func(a: List[int]) -> None:
    global ans
    x = 1
    for i in a:
        x = x * A[i] % mod
    ans += x
enumerate_cliques(N, edges, func)
wtn(ans % mod)