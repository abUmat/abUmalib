# my module
from misc.fastio import *
from fps.fps998244353 import *
# my module
N = rd()
C = Binomial(MOD, N + 10)
s2 = stirling2(N, C)
wtnl(s2)