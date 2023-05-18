# https://judge.yosupo.jp/problem/convolution_mod
# my module
from misc.fastio import *
from ntt.ntt998244353 import *
# my module
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
wtnl(multiply(A, B))