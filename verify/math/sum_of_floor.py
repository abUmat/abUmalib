# https://judge.yosupo.jp/problem/sum_of_floor_of_linear
# my module
from misc.fastio import *
from mymath.sum_of_floor import *
# my module
T = rd()
for _ in range(T):
    n, m, a, b = rd(), rd(), rd(), rd()
    wtn(sum_of_floor(n, m, a, b))