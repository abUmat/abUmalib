# https://judge.yosupo.jp/problem/assignment
# my module
from misc.fastio import *
from graph.mcf_graph import *
# my module
inf = 1001001001
N = rd()
graph = MCFGraph((N << 1) + 2)
s = N << 1
t = N << 1 | 1
for i in range(N):
    graph.add_edge(s, i, 1, 0)
    graph.add_edge(i + N, t, 1, 0)
for i in range(N):
    for j in range(N):
        c = rd()
        graph.add_edge(i, N + j, 1, c + inf)
flow, cost = graph.flow(s, t, N)
wtn(cost - inf * N)
ans = [0] * N
for src, dst, cap, flow, cost in graph.edges():
    if flow == 1 and cost:
        ans[src] = dst - N
wtnl(ans)
