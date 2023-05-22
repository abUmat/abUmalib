# https://judge.yosupo.jp/problem/lcm_convolution
# my module
from misc.fastio import *
from multiplicative_function.gcd_lcm_convolution import *
# my module
mod = 998244353
N = rd()
A = [0] + rdl(N)
B = [0] + rdl(N)
C = lcm_convolution(A, B, mod)
wtnl(C[1:])