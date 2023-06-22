# https://judge.yosupo.jp/problem/point_add_rectangle_sum
# my module
from misc.fastio import *
from data_structure_2d.static_rectangle_sum import *
# my module
N, Q = rd(), rd()
rect = StaticRectangleSum(N, Q)
for _ in range(N):
    x, y, w = rd(), rd(), rd()
    rect.add_point(x, y, w)
for _ in range(Q):
    l, d, r, u = rd(), rd(), rd(), rd()
    rect.add_query(l, d, r, u)
res = rect.solve()
for x in res: wtn(x)