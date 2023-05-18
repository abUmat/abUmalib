# https://judge.yosupo.jp/problem/bernoulli_number
# my module
from misc.fastio import *
from math998244353.fps_famous_series import *
# my module
N = rd()
C = Binomial(MOD, N + 10)
b = bernoulli(rd(), C)
wtnl(b)