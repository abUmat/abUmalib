# https://judge.yosupo.jp/problem/multipoint_evaluation
# my module
from misc.fastio import *
from math998244353.multieval import *
# my module
N, M = rd(), rd()
f = rdl(N)
xs = rdl(M)
wtnl(multipoint_evaluation(f, xs))