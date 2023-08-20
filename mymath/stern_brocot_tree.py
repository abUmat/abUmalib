# my module
from misc.typing_template import *
from mymath.gcd_lcm import *
# my module
# https://nyaannyaan.github.io/library/math/stern-brocot-tree.hpp
class SternBrocotTreeNode:
    def __init__(self, x: int=0, y: int=0) -> None:
        self.lx = 0
        self.ly = 1
        self.x = 1
        self.y = 1
        self.rx = 1
        self.ry = 0
        self.seq: Vector = []
        if not x and not y:
            return
        assert(1 <= x and 1 <= y)
        g = gcd2(x, y)
        x //= g
        y //= g
        while x and y:
            if x > y:
                d, x = divmod(x, y)
                self.go_right(d - (0 if x else 1))
            else:
                d, y = divmod(y, x)
                self.go_left(d - (0 if y else 1))

    def get(self) -> Pair:
        return self.x, self.y
    
    def lower_bound(self) -> Pair:
        return self.lx, self.ly
    
    def upper_bound(self) -> Pair:
        return self.rx, self.ry
    
    def depth(self) -> int:
        return sum(abs(s) for s in self.seq)
    
    def go_left(self, d: int=1) -> None:
        if d <= 0:
            return
        if (not self.seq) or self.seq[-1] > 0:
            self.seq.append(0)
        self.seq[-1] -= d
        self.rx += self.lx * d
        self.ry += self.ly * d
        self.x = self.rx + self.lx
        self.y = self.ry + self.ly

    def go_right(self, d: int=1) -> None:
        if d <= 0:
            return
        if (not self.seq) or self.seq[-1] < 0:
            self.seq.append(0)
        self.seq[-1] += d
        self.lx += self.rx * d
        self.ly += self.ry * d
        self.x = self.rx + self.lx
        self.y = self.ry + self.ly

    def go_parent(self, d: int=1) -> bool:
        if d <= 0:
            return 1
        lx, ly, x, y, rx, ry = self.lx, self.ly, self.x, self.y, self.rx, self.ry
        while d:
            if not self.seq:
                self.lx, self.ly, self.x, self.y, self.rx, self.ry = lx, ly, x, y, rx, ry
                return 0
            d2 = min(d, abs(self.seq[-1]))
            if self.seq[-1] > 0:
                x -= rx * d2
                y -= ry * d2
                lx = x - rx
                ly = y - ry
                self.seq[-1] -= d2
            else:
                x -= lx * d2
                y -= ly * d2
                rx = x - lx
                ry = y - ly
                self.seq[-1] += d2
            d -= d2
            if not self.seq[-1]:
                self.seq.pop()
            if not d2:
                break
        self.lx, self.ly, self.x, self.y, self.rx, self.ry = lx, ly, x, y, rx, ry
        return 1
    
    @staticmethod
    def lca(lhs, rhs):
        n = SternBrocotTreeNode()
        for i in range(min(len(lhs.seq), len(rhs.seq))):
            val1, val2 = lhs.seq[i], rhs.seq[i]
            if (val1 < 0) != (val2 < 0):
                break
            if val1 < 0:
                n.go_left(min(-val1, -val2))
            if val1 > 0:
                n.go_right(min(val1, val2))
            if val1 != val2:
                break
        return n
    
    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y
    
    def __le__(self, __value: object) -> bool:
        return self.x * __value.y < self.y * __value.x
    
    def __ge__(self, __value: object) -> bool:
        return self.x * __value.y > self.y * __value.x
