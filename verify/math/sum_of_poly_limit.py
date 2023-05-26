# https://judge.yosupo.jp/problem/sum_of_exponential_times_polynomial_limit
# my module
from misc.fastio import *
from fps.sum_of_exponential_times_poly import *
# my module
mod = 998244353
r, d = rd(), rd()
wtn(sum_of_exp_limit2(d, r, Binomial(mod, d + 10)))