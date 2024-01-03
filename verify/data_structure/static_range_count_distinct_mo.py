# https://judge.yosupo.jp/problem/static_range_count_distinct
# my module
from misc.fastio import *
from misc.mo import *
# my module
N, Q = rd(), rd()
A = rdl(N)
# 座圧
dic = {a:i for i, a in enumerate(sorted(set(A)))}
A = [dic[a] for a in A]
cnt = [0] * len(dic)
res = 0
def add(idx: int):
    global res
    a = A[idx]
    if not cnt[a]:
        res += 1
    cnt[a] += 1
def remove(idx: int):
    global res
    a = A[idx]
    cnt[a] -= 1
    if not cnt[a]:
        res -= 1
def get() -> int:
    return res

W = max(1, N / max(1, (Q * 2 / 3) ** 0.5))
mo = Mo(Q, add, add, remove, remove, get)
for i in range(Q):
    l, r = rd(), rd()
    mo.add_query(l, r, i, W)
wtnl(mo.solve())
