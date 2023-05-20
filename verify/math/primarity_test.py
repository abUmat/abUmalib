# https://judge.yosupo.jp/problem/primarity_test
# my module
from misc.fastio import *
from prime.is_prime import *
# my module
Q = rd()
for _ in range(Q):
    if is_prime(rd()):
        wtn("Yes")
    else:
        wtn("No")