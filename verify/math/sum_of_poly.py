# https://judge.yosupo.jp/problem/sum_of_exponential_times_polynomial
# my module
from misc.fastio import *
from fps.sum_of_exponential_times_poly import *
# my module
mod = 998244353
r, d, n = rd(), rd(), rd()
wtn(sum_of_exp2(d, r, n, Binomial(mod, d + 10)))