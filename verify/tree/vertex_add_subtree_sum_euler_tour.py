# https://judge.yosupo.jp/problem/vertex_add_subtree_sum
# my module
from misc.fastio import *
from tree.euler_tour import *
# my module
N, Q = rd(), rd()
A = rdl(N)
P = rdl(N - 1)
G = [[] for _ in range(N)]
for u, v in enumerate(P):
    u += 1
    G[u].append(v)
    G[v].append(u)
tree = EulerTour(G)
tree.build(A)
for _ in range(Q):
    cmd = rd()
    if cmd:
        u = rd()
        wtn(tree.query_subtree(u))
    else:
        p, x = rd(), rd()
        tree.add(p, x)
