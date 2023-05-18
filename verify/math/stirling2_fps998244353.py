# https://judge.yosupo.jp/problem/stirling_number_of_the_second_kind
# my module
from misc.fastio import *
from fps.fps998244353 import *
# my module
N = rd()
C = Binomial(MOD, N + 10)
s2 = stirling2(N, C)
wtnl(s2)