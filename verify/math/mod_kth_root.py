# https://judge.yosupo.jp/problem/kth_root_mod
# my module
from misc.fastio import *
from modulo.mod_kth_root import *
# my module
T = rd()
for _ in range(T):
    k, y, p = rd(), rd(), rd()
    wtn(kth_root(y, k, p))