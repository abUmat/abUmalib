# https://judge.yosupo.jp/problem/matrix_det
# my module
from misc.fastio import *
from matrix.black_box_linear_algebra import *
# my module
mod = 998244353
N = rd()
mat = ModMatrix(N, mod)
mat.mat = [rdl(N) for _ in range(N)]
wtn(fast_det(mat))