# https://judge.yosupo.jp/problem/staticrmq
# my module
from misc.fastio import *
from data_structure.sparse_table import *
# my module
N, Q = rd(), rd()
st = SparseTable(rdl(N))
for _ in range(Q): wtn(st.query(rd(), rd()))