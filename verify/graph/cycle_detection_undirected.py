# https://judge.yosupo.jp/problem/cycle_detection_undirected
# my module
from misc.fastio import *
from graph.cycle_detection import *
# my module
from collections import defaultdict
N, M = rd(), rd()
G = [[] for _ in range(N)]
memo = defaultdict(list)
for i in range(M):
    u, v = rd(), rd()
    if u > v: u, v = v, u
    G[u].append(v)
    G[v].append(u)
    memo[u << 20 | v].append(i)
cycle = cycle_detection(G, 0)
if not cycle:
    wtn(-1)
    exit()
wtn(len(cycle))
vs = []
es = []
for u, v in cycle:
    vs.append(u)
    if u > v: u, v = v, u
    edges = memo[u << 20 | v]
    es.append(edges.pop())
wtnl(vs)
wtnl(es)