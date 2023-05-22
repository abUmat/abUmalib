# https://judge.yosupo.jp/problem/convolution_mod_2_64
# my module
from misc.fastio import *
from ntt.arbitrary_ntt import *
# my module
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
mask32 = 0xffffffff
mask64 = 0xffffffffffffffff
a_upper = [x >> 32 for x in A]
a_lower = [x & mask32 for x in A]
b_upper = [x >> 32 for x in B]
b_lower = [x & mask32 for x in B]
res = ArbitraryNTT.multiply(a_lower, b_lower, 1 << 64)
aubl = ArbitraryNTT.multiply(a_upper, b_lower, 1 << 32)
albu = ArbitraryNTT.multiply(a_lower, b_upper, 1 << 32)
for i, x in enumerate(res):
    tmp = aubl[i] + albu[i] & mask32
    wt(((tmp << 32) + res[i]) & mask64)
    wt(' ')
wt('\n')