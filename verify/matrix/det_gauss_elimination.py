# https://judge.yosupo.jp/problem/matrix_det
# my module
from misc.fastio import *
from matrix.gauss_elimination import *
# my module
mod = 998244353
N = rd()
A = [rdl(N) for _ in range(N)]
_, det = gauss_elimination(A, mod)
wtn(det)