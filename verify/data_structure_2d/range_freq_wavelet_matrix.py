# my module
from misc.fastio import *
from data_structure_2d.wavelet_matrix import *
# my module
N, Q = rd(), rd()
A = rdl(N)
wm = WaveletMatrix(N, A)
wm.build()
for _ in range(Q):
    l, r, x = rd(), rd(), rd()
    wtn(wm.range_freq(l, r, x, x + 1))