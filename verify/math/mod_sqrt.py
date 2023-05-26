# https://judge.yosupo.jp/problem/sqrt_mod
# my module
from misc.fastio import *
from modulo.mod_sqrt import *
# my module
T = rd()
for _ in range(T):
    y, p = rd(), rd()
    wtn(mod_sqrt(y, p))