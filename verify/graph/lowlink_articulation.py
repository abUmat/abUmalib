# https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=GRL_3_A&lang=ja
# my module
from misc.fastio import *
from graph.lowlink import *
# my module
import sys
sys.setrecursionlimit(10**8)
N, M = rd(), rd()
G = [[] for _ in range(N)]
for _ in range(M):
    u, v = rd(), rd()
    G[u].append(v)
    G[v].append(u)
low = LowLink(G)
low.articulation.sort()
for v in low.articulation:
    wtn(v)