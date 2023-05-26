# https://judge.yosupo.jp/problem/line_add_get_min
# my module
from misc.fastio import *
from segment_tree.li_chao_tree import *
# my module
N, Q = rd(), rd()
A = []
B = []
for _ in range(N):
    a, b = rd(), rd()
    A.append(a)
    B.append(b)
C = [0] * Q
D = [0] * Q
E = [0] * Q
xs = []
for i in range(Q):
    cmd = rd()
    C[i] = cmd
    if cmd:
        d = rd()
        D[i] = d
        xs.append(d)
    else:
        D[i] = rd()
        E[i] = rd()
lichao = LiChaoTree(xs)
while A: lichao.update(A.pop(), B.pop())
for i in range(Q):
    if C[i]:
        wtn(lichao.query(D[i]))
    else:
        lichao.update(D[i], E[i])