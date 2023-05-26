# https://judge.yosupo.jp/problem/longest_increasing_subsequence
# my module
from misc.fastio import *
from misc.longest_increasing_subsequence import *
# my module
N = rd()
A = rdl(N)
l, ind = lis(A)
wtn(l)
wtnl(ind)