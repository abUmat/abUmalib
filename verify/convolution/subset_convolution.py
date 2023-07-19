# https://judge.yosupo.jp/problem/subset_convolution
# my module
from misc.fastio import *
from set_function.subset_convolution import *
# my module
mod = 998244353
N = rd()
A = rdl(1 << N)
B = rdl(1 << N)
sc = SubsetConvolution(20, mod)
wtnl(sc.multiply(A, B))