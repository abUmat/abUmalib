# https://judge.yosupo.jp/problem/multipoint_evaluation
# my module
from misc.fastio import *
from math998244353.multieval_fast import *
# my module
N, M = rd(), rd()
C = rdl(N)
P = rdl(M)
wtnl(multipoint_evaluation_fast(C, P))