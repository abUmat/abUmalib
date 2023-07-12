# https://judge.yosupo.jp/problem/convolution_mod_2_64
# my module
from misc.fastio import *
from ntt.complex_fft import *
# my module
n, m = rd(), rd()
a = rdl(n)
b = rdl(m)
wtnl(CooleyTukey().karatsuba_mod2_64(a, b))