# my module
from lct.lazy_reversible_bbst_base import *
# my module

class LazyReversibleSplayTreeNode:
    def __init__(self, e, id_, val=None, lazy=None):
        self.l = None
        self.r = None
        self.p = None
        if val: self.key = val; self.sum = val
        else: self.key = e; self.sum = e
        if lazy: self.lazy = lazy
        else: self.lazy = id_
        self.cnt = 1
        self.rev = 0

class LazyReversibleSplayTree(LazyReversibleBBST):
    def __init__(self, e, id_, op, mapping, composition, ts):
        super().__init__(LazyReversibleSplayTreeNode, e, id_, op, mapping, composition, ts)
