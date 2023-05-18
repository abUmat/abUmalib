# https://judge.yosupo.jp/problem/convolution_mod
# my module
from misc.fastio import *
from ntt.ntt import *
# my module
mod = 998244353
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
ntt = NTT(mod)
wtnl(ntt.multiply(A, B))