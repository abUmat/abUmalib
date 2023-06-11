# https://judge.yosupo.jp/problem/two_edge_connected_components
# my module
from misc.fastio import *
from graph.two_edge_connected_components import *
# my module
import sys
sys.setrecursionlimit(10**8)
N, M = rd(), rd()
G = [[] for _ in range(N)]
for i in range(M):
    u, v = rd(), rd()
    if u > v: u, v = v, u
    G[u].append(v)
    G[v].append(u)
low = TwoEdgeConnectedComponents(G)
s = len(low.groups)
wtn(s)
for i in range(s):
    wt(len(low.groups[i])); wt(' ')
    wtnl(low.groups[i])