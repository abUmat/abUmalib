# https://judge.yosupo.jp/problem/matrix_rank
# my module
from misc.fastio import *
from matrix.gauss_elimination import *
# my module
N, M = rd(), rd()
mat = [rdl(M) for _ in range(N)]
MOD = 998244353
rank, det = gauss_elimination(mat, MOD)
wtn(rank)
