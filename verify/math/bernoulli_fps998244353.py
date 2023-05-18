# https://judge.yosupo.jp/problem/bernoulli_number
# my module
from misc.fastio import *
from fps.fps998244353 import *
# my module
N = rd()
C = Binomial(MOD, N + 10)
b = bernoulli(rd(), C)
wtnl(b)