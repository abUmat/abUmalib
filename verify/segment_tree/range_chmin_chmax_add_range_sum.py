# https://judge.yosupo.jp/problem/range_chmin_chmax_add_range_sum
# my module
from misc.fastio import *
from segment_tree.segment_tree_beats import *
# my module
N, Q = rd(), rd()
A = rdl(N)
seg = SegmentTreeBeats(N, A)
for _ in range(Q):
    cmd = rd()
    if not cmd:
        l, r, b = rd(), rd(), rd()
        seg.range_chmin(l, r, b)
    elif cmd == 1:
        l, r, b = rd(), rd(), rd()
        seg.range_chmax(l, r, b)
    elif cmd == 2:
        l, r, b = rd(), rd(), rd()
        seg.range_add(l, r, b)
    elif cmd == 3:
        l, r = rd(), rd()
        wtn(seg.get_sum(l, r))