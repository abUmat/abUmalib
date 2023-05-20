# https://judge.yosupo.jp/problem/polynomial_interpolation
# my module
from misc.fastio import *
from fps.ntt_friendly_fps import *
from fps.polynomial_interpolation import *
# my module
mod = 998244353
N = rd()
xs = rdl(N)
ys = rdl(N)
wtnl(polynomial_interpolation(xs, ys, mod))