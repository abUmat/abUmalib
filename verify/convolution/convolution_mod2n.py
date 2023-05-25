# https://judge.yosupo.jp/problem/mul_mod2n_convolution
# my module
from misc.fastio import *
from multiplicative_function.convolution_mod2n import *
# my module
mod = 998244353
N = rd()
A = rdl(1 << N)
B = rdl(1 << N)
wtnl(multiplicative_convolution_mod2n(A, B, mod))
