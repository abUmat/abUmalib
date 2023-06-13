# https://judge.yosupo.jp/problem/sparse_matrix_det
# my module
from misc.fastio import *
from matrix.bbla998244353 import *
# my module
N, K = rd(), rd()
mat = SparseMatrix(N)
for _ in range(K):
    i, j, x = rd(), rd(), rd()
    mat.add(i, j, x)
wtn(fast_det(mat))