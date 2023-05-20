# https://judge.yosupo.jp/problem/polynomial_taylor_shift
# my module
from misc.fastio import *
from fps.arbitrary_fps import *
from fps.taylor_shift import *
# my module
mod = 998244353
N, c = rd(), rd()
A = rdl(N)
wtnl(taylor_shift(A, c, Binomial(mod, N)))