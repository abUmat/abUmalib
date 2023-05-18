# https://judge.yosupo.jp/problem/polynomial_taylor_shift
# my module
from misc.fastio import *
from math998244353.taylor_shift import *
# my module
N, c = rd(), rd()
A = rdl(N)
wtnl(taylor_shift(A, c, Binomial(MOD, N)))