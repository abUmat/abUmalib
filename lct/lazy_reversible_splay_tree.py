# my module
from lct.lazy_reversible_bbst_base import *
# my module
class LazyReversibleSplayTreeNode:
    def __init__(self, val: int, lazy: int) -> None:
        self.l = None
        self.r = None
        self.p = None
        self.key = val; self.sum = val
        self.lazy = lazy
        self.cnt = 1
        self.rev = 0

class LazyReversibleSplayTree(LazyReversibleBBST):
    def __init__(self, e: int, id_: int, op: Callable[[int, int], int], mapping: Callable[[int, int], int], composition: Callable[[int, int], int], ts: Callable[[int], int]) -> None:
        '''
        e: identity element of op
        id_: identity mapping s.t. id(x) == x
        op: S*S -> S
        mapping: mapping(f, x) := f(x)
        composition: composition(f, g) := fog
        '''
        super().__init__(LazyReversibleSplayTreeNode, e, id_, op, mapping, composition, ts)
