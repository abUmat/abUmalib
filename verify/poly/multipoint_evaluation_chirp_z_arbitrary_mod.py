# https://judge.yosupo.jp/problem/multipoint_evaluation_on_geometric_sequence
# my module
from misc.fastio import *
from ntt.chirp_z import *
# my module
mod = 998244353
N, M, a, r = rd(), rd(), rd(), rd()
c = rdl(N)
wtnl(chirp_z(mod, c, r, M, a))