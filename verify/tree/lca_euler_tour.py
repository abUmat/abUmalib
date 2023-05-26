# https://judge.yosupo.jp/problem/lca
# my module
from misc.fastio import *
from tree.euler_tour import *
# my module
N, Q = rd(), rd()
P = rdl(N - 1)
G = [[] for _ in range(N)]
for u, v in enumerate(P):
    G[u + 1].append(v)
    G[v].append(u + 1)
tree = EulerTour(G)
for _ in range(Q): wtn(tree.lca(rd(), rd()))
