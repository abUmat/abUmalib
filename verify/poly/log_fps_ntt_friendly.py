# https://judge.yosupo.jp/problem/log_of_formal_power_series
# my module
from misc.fastio import *
from fps.ntt_friendly_fps import *
# my module
mod = 998244353
fps = FPS(mod)
N = rd()
A = rdl(N)
wtnl(fps.log(A))