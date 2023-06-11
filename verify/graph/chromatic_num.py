# https://judge.yosupo.jp/problem/chromatic_number
# my module
from misc.fastio import *
from graph.chromatic_number import *
# my module
N, M = rd(), rd()
G = [[] for _ in range(N)]
for _ in range(M):
    u, v = rd(), rd()
    G[u].append(v)
    G[v].append(u)
wtn(chromatic_number(G))