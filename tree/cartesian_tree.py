# my module
from misc.typing_template import *
# my module
# https://nyaannyaan.github.io/library/tree/cartesian-tree.hpp
def cartesian_tree(a: Vector) -> Vector:
    N = len(a)
    p = [-1] * N
    st = [0] * N
    idx = -1
    for i, x in enumerate(a):
        prv = -1
        while idx != -1 and x < a[st[idx]]:
            prv = st[idx]
            idx -= 1
        if prv != -1: p[prv] = i
        if idx != -1: p[i] = st[idx]
        idx += 1
        st[idx] = i
    return p