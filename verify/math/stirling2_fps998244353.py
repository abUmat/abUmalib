# https://judge.yosupo.jp/problem/stirling_number_of_the_second_kind
# my module
from misc.fastio import *
from math998244353.fps_famous_series import *
# my module
N = rd()
C = Binomial(MOD, N + 10)
s2 = stirling2(N, C)
wtnl(s2)