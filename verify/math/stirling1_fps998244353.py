# https://judge.yosupo.jp/problem/stirling_number_of_the_first_kind
# my module
from misc.fastio import *
from math998244353.fps_famous_series import *
# my module
N = rd()
C = Binomial(MOD, N)
s1 = stirling1(N, C)
for i in range(N)[::-2]: s1[i] = -s1[i] % MOD
wtnl(s1)