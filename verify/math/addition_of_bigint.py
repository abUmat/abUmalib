# https://judge.yosupo.jp/problem/addition_of_big_integers
# my module
from misc.fastio import *
from mymath.bigint import *
# my module
T = rd()
for _ in range(T):
    a, b = rds(), rds()
    a = bigint(a)
    b = bigint(b)
    wtn(a + b)
