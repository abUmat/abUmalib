# https://judge.yosupo.jp/problem/kth_term_of_linearly_recurrent_sequence
# my module
from misc.fastio import *
from math998244353.kitamasa import *
# my module
d, k = rd(), rd()
a = rdl(d)
c = rdl(d)
c[:0] = [0]
c = FPS.sub([1], c)
wtn(kitamasa(k, c, a))