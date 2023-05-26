# https://judge.yosupo.jp/problem/vertex_add_path_sum
# my module
from misc.fastio import *
from tree.euler_tour import *
# my module
N, Q = rd(), rd()
A = rdl(N)
G = [[] for _ in range(N)]
for _ in range(N - 1):
    u, v = rd(), rd()
    G[u].append(v)
    G[v].append(u)
tree = EulerTour(G)
tree.build(A)
for _ in range(Q):
    cmd = rd()
    if cmd:
        u, v = rd(), rd()
        wtn(tree.query_vertex(u, v))
    else:
        p, x = rd(), rd()
        tree.add(p, x)
