# https://judge.yosupo.jp/problem/convolution_mod_1000000007
# my module
from misc.fastio import *
from ntt.complex_fft import *
# my module
mod = 1_000_000_007
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
wtnl(CooleyTukey().karatsuba(A, B, mod))