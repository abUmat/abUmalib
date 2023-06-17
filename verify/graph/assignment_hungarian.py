# https://judge.yosupo.jp/problem/assignment
# my module
from misc.fastio import *
from graph.hungarian import *
# my module
N = rd()
A = [rdl(N) for _ in range(N)]
total, row = hungarian(A)
wtn(total)
wtnl(row)