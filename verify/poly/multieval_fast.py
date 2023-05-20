# https://judge.yosupo.jp/problem/multipoint_evaluation
# my module
from misc.fastio import *
from fps.multieval_fast import *
# my module
mod = 998244353
N, M = rd(), rd()
C = rdl(N)
P = rdl(M)
wtnl(multipoint_evaluation_fast(C, P, mod))