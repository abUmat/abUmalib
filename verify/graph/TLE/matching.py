# https://judge.yosupo.jp/problem/bipartitematching
# my module
from misc.fastio import *
from graph.matching import *
# my module
L, R, M = rd(), rd(), rd()
graph = Matching(L, R)
for i in range(M):
    frm, to = rd(), rd()
    graph.add_edge(frm, to)
wtn(graph.flow())
es = graph.edges()
for e in es:
    wtnl(e)