# https://judge.yosupo.jp/problem/binomial_coefficient
# my module
from misc.fastio import *
from modulo.arbitrary_mod_binomial import *
# my module
T, m = rd(), rd()
binomi = ArbitraryModBinomial(m)
for _ in range(T): wtn(binomi(rd(), rd()))