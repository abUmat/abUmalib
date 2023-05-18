# https://judge.yosupo.jp/problem/sqrt_of_formal_power_series
# my module
from misc.fastio import *
from math998244353.fps_sqrt import *
# my module
N = rd()
A = rdl(N)
ans = sqrt(A)
wtnl(ans) if ans else wtn(-1)