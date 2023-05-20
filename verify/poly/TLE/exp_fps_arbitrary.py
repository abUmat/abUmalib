# https://judge.yosupo.jp/problem/exp_of_formal_power_series
# my module
from misc.fastio import *
from fps.arbitrary_fps import *
# my module
mod = 998244353
fps = FPS(mod)
N = rd()
A = rdl(N)
wtnl(fps.exp(A))