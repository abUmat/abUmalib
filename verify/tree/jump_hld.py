# https://judge.yosupo.jp/problem/jump_on_tree
# my module
from misc.fastio import *
from tree.heavy_light_decomposition import *
# my module
N, Q = rd(), rd()
G = [[] for _ in range(N)]
for i in range(N - 1):
    a, b = rd(), rd()
    G[a].append(b)
    G[b].append(a)
hld = HeavyLightDecomposition(G)
for _ in range(Q):
    s, t, i = rd(), rd(), rd()
    wtn(hld.la(s, t, i))