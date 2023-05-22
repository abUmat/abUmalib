# https://judge.yosupo.jp/problem/enumerate_primes
# my module
from misc.fastio import *
from prime.prime_enumerate import *
# my module
N, A, B = rd(), rd(), rd()
ps = prime_enumerate(N)
res = ps[B::A]
wtnl((len(ps), len(res)))
wtnl(res)