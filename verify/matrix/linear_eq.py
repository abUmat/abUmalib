# https://judge.yosupo.jp/problem/system_of_linear_equations
# my module
from misc.fastio import *
from matrix.linear_equation import *
# my module
mod = 998244353
N, M = rd(), rd()
A = [rdl(M) for _ in range(N)]
b = rdl(N)
v = linear_equation(A, b, mod)
wtn(len(v) - 1)
for x in v: wtnl(x)