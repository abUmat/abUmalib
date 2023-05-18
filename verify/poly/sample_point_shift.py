# https://judge.yosupo.jp/problem/shift_of_sampling_points_of_polynomial
# my module
from misc.fastio import *
from math998244353.sample_point_shift import *
# my module
N, M, c = rd(), rd(), rd()
f = rdl(N)
wtnl(sample_point_shift(f, c, M))