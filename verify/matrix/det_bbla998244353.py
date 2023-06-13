# https://judge.yosupo.jp/problem/matrix_det
# my module
from misc.fastio import *
from matrix.bbla998244353 import *
# my module
N = rd()
mat = ModMatrix(N)
mat.mat = [rdl(N) for _ in range(N)]
wtn(fast_det(mat))