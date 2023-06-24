# my module
from misc.typing_template import *
# my module
class TreeHash:
    _MOD = 0x1fffffffffffffff # (1<<61)-1
    _MASK30 = 0x3fffffff # (1<<30)-1
    _MASK31 = 0x7fffffff # (1<<31)-1
    _MASK61 = _MOD

    @classmethod
    def _mul(cls, a: int, b: int) -> int:
        # fast multiply and modulo
        # https://qiita.com/keymoon/items/11fac5627672a6d6a9f6
        au, ad = a >> 31, a & cls._MASK31
        bu, bd = b >> 31, b & cls._MASK31
        mid = ad * bu + au * bd
        midu, midd = mid >> 30, mid & cls._MASK30
        x = (au * bu << 1) + midu + (midd << 31) + ad * bd
        xu, xd = x >> 61, x & cls._MASK61
        res = xu + xd
        return res if res < cls._MOD else res - cls._MOD

    def __init__(self, g: Graph, root: int=0) -> None:
        self.g = g
        n = len(g)
        assert(n < 1 << 20)
        from random import randint
        def rng():
            rngx = randint(0, 0xffffffff)
            while 1:
                rngx ^= rngx << 13 & 0xffffffff
                rngx ^= rngx >> 17 & 0xffffffff
                rngx ^= rngx << 5 & 0xffffffff
                yield rngx & 0xffffffff
        rand = rng()
        self.hash = [0] * n
        self.depth = [0] * n
        self.xs = [next(rand) for _ in range(n)]
        self._dfs(root, root)

    def _dfs(self, _c: int, _p: int) -> None:
        stack = [_c << 20 | _p]
        while stack:
            cp = stack.pop()
            c, p = cp >> 20, cp & 0xfffff
            if c >= 0:
                stack.append(~c << 20 | p)
                for d in self.g[c]:
                    if d != p:
                        stack.append(d << 20 | c)
            else:
                c = ~c
                dep = 0
                for d in self.g[c]:
                    if d != p:
                        dep = max(dep, self.depth[d] + 1)
                self.depth[c] = dep
                x = self.xs[dep]
                h = 1
                for d in self.g[c]:
                    if d != p:
                        h = self._mul(h, x + self.hash[d])
                self.hash[c] = h
