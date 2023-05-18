# https://judge.yosupo.jp/problem/polynomial_interpolation
# my module
from misc.fastio import *
from math998244353.polynomial_interpolation import *
# my module
N = rd()
xs = rdl(N)
ys = rdl(N)
wtnl(polynomial_interpolation(xs, ys))