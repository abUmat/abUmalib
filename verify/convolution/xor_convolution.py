# https://judge.yosupo.jp/problem/bitwise_xor_convolution
# my module
from misc.fastio import *
from set_function.xor_convolution import *
# my module
mod = 998244353
N = rd()
A = rdl(1 << N)
B = rdl(1 << N)
wtnl(xor_convolution(A, B, mod))