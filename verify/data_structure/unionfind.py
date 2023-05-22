# https://judge.yosupo.jp/problem/unionfind
# my module
from misc.fastio import *
from data_structure.unionfind import *
# my module
N, Q = rd(), rd()
uf = UnionFind(N)
for _ in range(Q):
    t = rd()
    if t:
        u, v = rd(), rd()
        wtn(int(uf.same(u, v)))
    else:
        u, v = rd(), rd()
        uf.union(u, v)