# https://judge.yosupo.jp/problem/stirling_number_of_the_first_kind
# my module
from misc.fastio import *
from fps.fps_famous_series import *
from fps.arbitrary_fps import *
# my module
mod = 998244353
N = rd()
C = Binomial(mod, N)
s1 = stirling1(N, C)
for i in range(N)[::-2]: s1[i] = -s1[i] % mod
wtnl(s1)