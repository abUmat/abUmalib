# https://judge.yosupo.jp/problem/multipoint_evaluation
# my module
from misc.fastio import *
from fps.fps998244353 import *
# my module
N, M = rd(), rd()
C = rdl(N)
P = rdl(M)
wtnl(multipoint_evaluation(C, P))