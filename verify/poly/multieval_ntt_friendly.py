# https://judge.yosupo.jp/problem/multipoint_evaluation
# my module
from misc.fastio import *
from fps.ntt_friendly_fps import *
from fps.multieval import *
# my module
mod = 998244353
N, M = rd(), rd()
f = rdl(N)
xs = rdl(M)
wtnl(multipoint_evaluation(f, xs, mod))