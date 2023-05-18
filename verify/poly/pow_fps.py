# https://judge.yosupo.jp/problem/pow_of_formal_power_series
# my module
from misc.fastio import *
from math998244353.fps import *
# my module
N, M = rd(), rd()
A = rdl(N)
wtnl(fps_pow(A, M))