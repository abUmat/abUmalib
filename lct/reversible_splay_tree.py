# my module
from lct.splay_base import *
from lct.reversible_bbst_base import *
# my module
class ReversibleSplayTreeNode:
    def __init__(self, e: int):
        self.l = None
        self.r = None
        self.p = None
        self.key = e
        self.sum = e
        self.cnt = 1
        self.rev = 0

class ReversibleSplayTree(ReversibleBBST):
    def __init__(self, e: int, op: Callable[[int, int], int], ts: Callable[[int, int], int]):
        super().__init__(ReversibleSplayTreeNode, e, op, ts)
