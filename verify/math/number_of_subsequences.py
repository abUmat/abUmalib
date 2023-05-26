# https://judge.yosupo.jp/problem/number_of_subsequences
# my module
from misc.fastio import *
from misc.number_of_subsequences import *
# my module
mod = 998244353
N = rd()
A = rdl(N)
wtn(number_of_subsequences(A, 0, mod))