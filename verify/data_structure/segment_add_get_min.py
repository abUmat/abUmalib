# https://judge.yosupo.jp/problem/segment_add_get_min
# my module
from misc.fastio import *
from segment_tree.li_chao_tree import *
# my module
N, Q = rd(), rd()
L, R, A, B = [], [], [], []
for _ in range(N):
    L.append(rd())
    R.append(rd())
    A.append(rd())
    B.append(rd())
C, D, E, F, G = [], [], [0] * Q, [0] * Q, [0] * Q
xs = []
for i in range(Q):
    cmd = rd()
    C.append(cmd)
    if cmd:
        d = rd()
        D.append(d)
        xs.append(d)
    else:
        D.append(rd())
        E[i] = rd()
        F[i] = rd()
        G[i] = rd()
xs.append(1 << 31)
xs.append(-1 << 31)
lichao = LiChaoTree(xs)
while L:
    lichao.update_segment(A.pop(), B.pop(), L.pop(), R.pop()-1)
for i in range(Q):
    if C[i]:
        res = lichao.query(D[i])
        if res == (1 << 60) - 1:
            wtn("INFINITY")
        else:
            wtn(res)
    else:
        lichao.update_segment(F[i], G[i], D[i], E[i]-1)