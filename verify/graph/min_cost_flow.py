# https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=GRL_6_B
# my module
from misc.fastio import *
from graph.mcf_graph import *
# my module
V, E, F = rd(), rd(), rd()
graph = MCFGraph(V)
for _ in range(E):
    u, v, c, d = rd(), rd(), rd(), rd()
    graph.add_edge(u, v, c, d)
flow, cost = graph.flow(0, V - 1, F)
if flow == F:
    wtn(cost)
else:
    wtn(-1)