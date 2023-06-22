# https://judge.yosupo.jp/problem/static_rectangle_add_rectangle_sum
# my module
from misc.fastio import *
from data_structure_2d.static_rectangle_add_rectangle_sum import *
# my module
mod = 998244353
N, Q = rd(), rd()
rectangle = StaticRectangleAddRectangleSum(N, Q)
for _ in range(N):
    rectangle.add_rectangle(rd(), rd(), rd(), rd(), rd())
for _ in range(Q):
    rectangle.add_query(rd(), rd(), rd(), rd())
for a in rectangle.solve():
    wtn(a)
