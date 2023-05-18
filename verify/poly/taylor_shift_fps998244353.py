# my module
from misc.fastio import *
from fps.fps998244353 import *
# my module
N, c = rd(), rd()
A = rdl(N)
wtnl(taylor_shift(A, c, Binomial(MOD, N)))