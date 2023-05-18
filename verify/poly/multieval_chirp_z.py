# https://judge.yosupo.jp/problem/multipoint_evaluation_on_geometric_sequence
# my module
from misc.fastio import *
from math998244353.chirp_z import *
# my module
N, M, a, r = rd(), rd(), rd(), rd()
c = rdl(N)
wtnl(chirp_z(c, r, M, a))