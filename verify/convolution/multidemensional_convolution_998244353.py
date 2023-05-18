# https://judge.yosupo.jp/problem/multivariate_convolution
# my module
from misc.fastio import *
from math998244353.multivariate_multiplication import *
# my module
K = rd()
base = rdl(K)
N = 1
for x in base: N *= x
A = rdl(N)
B = rdl(N)
wtnl(multivariate_multiplication(A, B, base))