# https://judge.yosupo.jp/problem/tetration_mod
# my module
from misc.fastio import *
from modulo.tetration import *
# my module
T = rd()
for _ in range(T):
    a, b, m = rd(), rd(), rd()
    wtn(tetration(a, b, m))