# my module
from misc.fastio import *
from data_structure_2d.wavelet_matrix import *
# my module
N, Q = rd(), rd()
A = rdl(N)
wm = WaveletMatrix(N, A)
for _ in range(Q): wtn(wm.kth_smallest(rd(), rd(), rd()))