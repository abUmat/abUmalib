# https://judge.yosupo.jp/problem/manhattanmst
# my module
from misc.fastio import *
from graph.manhattan_mst import *
# my module
N = rd()
X, Y = [0] * N, [0] * N
for i in range(N):
    X[i] = rd()
    Y[i] = rd()
G = manhattan_mst(X, Y)
ans = 0
edges = [0] * len(G)
for i, (ij, cost) in enumerate(G.items()):
    ans += cost
    edges[i] = ij
wtn(ans)
mask = (1 << 30) - 1
for ij in edges:
    i, j = ij >> 30, ij & mask
    wt(i); wt(' '); wtn(j)
