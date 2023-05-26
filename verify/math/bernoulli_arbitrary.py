# https://judge.yosupo.jp/problem/bernoulli_number
# my module
from misc.fastio import *
from fps.fps_famous_series import *
from fps.arbitrary_fps import *
# my module
mod = 998244353
N = rd()
C = Binomial(mod, N + 10)
b = bernoulli(N, C)
wtnl(b)