# https://judge.yosupo.jp/problem/composition_of_formal_power_series
# my module
from misc.fastio import *
from fps.ntt_friendly_fps import *
from fps.fps_composition import *
# my module
mod = 998244353
N = rd()
A = rdl(N)
B = rdl(N)
wtnl(composition(A, B, mod))