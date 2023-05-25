# https://judge.yosupo.jp/problem/multivariate_convolution_cyclic
# my module
from misc.fastio import *
from ntt.multivariate_multiplication_cyclic import *
# my module
p, K = rd(), rd()
base = rdl(K)
N = 1
for n in base: N *= n
f = rdl(N)
g = rdl(N)
wtnl(multivariate_multiplication_cyclic(f, g, base, p))