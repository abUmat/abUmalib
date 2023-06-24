# https://judge.yosupo.jp/problem/cycle_detection
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
    G[u].append(v)
    memo[u << 20 | v].append(i)
cycle = cycle_detection(G)
if not cycle:
    wtn(-1)
    exit()
wtn(len(cycle))
for p in cycle:
    v = memo[p[0] << 20 | p[1]]
    wtn(v.pop())