# https://judge.yosupo.jp/problem/matrix_det
# my module
from misc.fastio import *
from matrix.determinant import *
# my module
mod = 998244353
N = rd()
A = [rdl(N) for _ in range(N)]
wtn(determinant(A, mod))