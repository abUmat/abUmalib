# https://judge.yosupo.jp/problem/kth_term_of_linearly_recurrent_sequence
# my module
from misc.fastio import *
from fps.arbitrary_fps import *
from fps.kitamasa import *
# my module
mod = 998244353
d, k = rd(), rd()
a = rdl(d)
c = rdl(d)
c[:0] = [0]
c = FPS(mod).sub([1], c)
wtn(kitamasa(k, c, a, mod))