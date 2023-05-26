# https://judge.yosupo.jp/problem/kth_root_integer
# my module
from misc.fastio import *
from mymath.kth_root_integer import *
# my module
T = rd()
for _ in range(T):
    a, k = rd(), rd()
    wtn(kth_root_integer(a, k))