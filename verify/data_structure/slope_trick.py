# https://atcoder.jp/contests/abc127/submissions/42369457
# my module
from misc.fastio import *
from data_structure.slope_trick import *
# my module
Q = rd()
st = SlopeTrick()
for _ in range(Q):
    cmd = rd()
    if cmd == 1:
        a, b = rd(), rd()
        st.add_abs_xma(a)
        st.shift_y(b)
    else:
        wtnl(st.get_min())
