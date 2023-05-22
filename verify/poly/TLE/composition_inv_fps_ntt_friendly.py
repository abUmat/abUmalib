# https://judge.yosupo.jp/problem/compositional_inverse_of_formal_power_series
# my module
from misc.fastio import *
from fps.ntt_friendly_fps import *
from fps.fps_composition_inverse import *
# my module
mod = 998244353
N = rd()
A = rdl(N)
wtnl(composition_inverse(A, mod))