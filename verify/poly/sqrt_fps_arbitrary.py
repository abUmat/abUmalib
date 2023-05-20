# https://judge.yosupo.jp/problem/sqrt_of_formal_power_series
# my module
from misc.fastio import *
from fps.arbitrary_fps import *
from fps.fps_sqrt import *
# my module
mod = 998244353
N = rd()
A = rdl(N)
ans = fps_sqrt(A, mod)
if ans: wtnl(ans)
else: wtn(-1)