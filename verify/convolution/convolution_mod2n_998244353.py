# https://judge.yosupo.jp/problem/mul_mod2n_convolution
# my module
from misc.fastio import *
from math998244353.multiplicative_convolution_mod2n import *
# my module
N = rd()
A = rdl(1 << N)
B = rdl(1 << N)
wtnl(multiplicative_convolution_mod2n(A, B))
