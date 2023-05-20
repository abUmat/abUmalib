# https://judge.yosupo.jp/problem/convolution_mod
# my module
from misc.fastio import *
from math998244353.ntt import *
# my module
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
wtnl(NTT.multiply(A, B))