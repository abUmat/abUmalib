# https://judge.yosupo.jp/problem/inverse_matrix
# my module
from misc.fastio import *
from matrix.inverse_matrix import *
# my module
mod = 998244353
N = rd()
A = [rdl(N) for _ in range(N)]
inv = inverse_matrix(A, mod)
if not inv: wtn(-1)
for invi in inv:
    wtnl(invi)