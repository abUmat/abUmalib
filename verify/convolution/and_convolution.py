# https://judge.yosupo.jp/problem/bitwise_and_convolution
# my module
from misc.fastio import *
from set_function.and_convolution import *
# my module
mod = 998244353
N = rd()
A = rdl(1 << N)
B = rdl(1 << N)
wtnl(and_convolution(A, B, mod))