# https://judge.yosupo.jp/problem/convolution_mod
# my module
from misc.fastio import *
from math998244353.relaxed_convolution import *
# my module
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
A += [0] * (M - 1)
B += [0] * (N - 1)
conv = RelaxedConvolution(N + M - 2)
C = []
for i in range(N + M - 1):
    C.append(conv.get(A[i], B[i]))
wtnl(C)
