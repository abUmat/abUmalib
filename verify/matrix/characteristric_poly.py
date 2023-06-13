# https://judge.yosupo.jp/problem/characteristic_polynomial
# my module
from misc.fastio import *
from matrix.characteristric_poly import *
# my module
mod = 998244353
N = rd()
A = [rdl(N) for _ in range(N)]
charpoly = characteristic_polynomial(A, mod)
if charpoly[-1] != 1:
    for i in range(len(charpoly)):
        charpoly[i] = (-charpoly[i]) % mod
wtnl(charpoly)