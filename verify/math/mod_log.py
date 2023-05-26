# https://judge.yosupo.jp/problem/discrete_logarithm_mod
# my module
from misc.fastio import *
from modulo.mod_log import *
# my module
T = rd()
for _ in range(T):
    x, y, m = rd(), rd(), rd()
    wtn(mod_log(x, y, m))