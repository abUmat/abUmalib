# https://judge.yosupo.jp/problem/shift_of_sampling_points_of_polynomial
# my module
from misc.fastio import *
from fps.arbitrary_fps import *
from fps.sample_point_shift import *
# my module
mod = 998244353
N, M, c = rd(), rd(), rd()
f = rdl(N)
wtnl(sample_point_shift(f, c, mod, M))