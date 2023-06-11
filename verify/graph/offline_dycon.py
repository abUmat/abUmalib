# https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=2235
# my module
from misc.fastio import *
from graph.offline_dynamic_connectivity import *
# my module
N, Q = rd(), rd()
cmd = [0] * Q
U = [0] * Q
V = [0] * Q
for i in range(Q):
    cmd[i] = rd()
    U[i] = rd()
    V[i] = rd()
dycon = OffLineDynamicConnectivity(N, Q)
for i in range(Q):
    if cmd[i] == 1: dycon.add_edge(i, U[i], V[i])
    if cmd[i] == 2: dycon.del_edge(i, U[i], V[i])
dycon.build()
ans = []
def add(u, v): return
def delete(u, v): return
def query(i):
    if cmd[i] == 3:
        ans.append(dycon.uf.same(U[i], V[i]))
dycon.run(add, delete, query)
for x in ans:
    if x: wtn("YES")
    else: wtn("NO")