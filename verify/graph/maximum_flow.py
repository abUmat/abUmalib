# https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=GRL_6_A
# my module
from misc.fastio import *
from graph.mf_graph import *
# my module
N, M = rd(), rd()
g = MFGraph(N)
for _ in range(M):
    u, v, cap = rd(), rd(), rd()
    g.add_edge(u, v, cap)
wtn(g.flow(0, N - 1))