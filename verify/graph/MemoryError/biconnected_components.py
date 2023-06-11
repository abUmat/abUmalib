# https://judge.yosupo.jp/problem/biconnected_components
# my module
from misc.fastio import *
from graph.biconnected_components import *
# my module
from itertools import chain
import sys
sys.setrecursionlimit(10**8)
N, M = rd(), rd()
G = [[] for _ in range(N)]
for i in range(M):
    u, v = rd(), rd()
    if u > v: u, v = v, u
    G[u].append(v)
    G[v].append(u)
bc = BiConnectedComponents(G)
s = len(bc.bc)
rem = set(range(N))
ans = []
for i in range(s):
    res = set(chain.from_iterable(bc.bc[i]))
    ans.append(res)
    rem -= res
if rem:
    s += len(rem)
    for v in rem:
        ans.append([v])
wtn(s)
for x in ans:
    wt(len(x))
    wt(' ')
    wtnl(x)