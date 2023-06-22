# https://judge.yosupo.jp/problem/lca
# my module
from misc.fastio import *
from tree.heavy_light_decomposition import *
# my module
N, Q = rd(), rd()
G = [[] for _ in range(N)]
for i in range(N - 1):
    G[rd()].append(i + 1)
hld = HeavyLightDecomposition(G)
for _ in range(Q):
    u, v = rd(), rd()
    wtn(hld.lca(u, v))