# https://judge.yosupo.jp/problem/stirling_number_of_the_second_kind
# my module
from misc.fastio import *
from fps.fps_famous_series import *
from fps.arbitrary_fps import *
# my module
mod = 998244353
N = rd()
C = Binomial(mod, N + 10)
s2 = stirling2(N, C)
wtnl(s2)