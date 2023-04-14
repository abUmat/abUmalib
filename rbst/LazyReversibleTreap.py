from time import time
start = time()
from atexit import register
from os import read, write
import sys
sys.setrecursionlimit(10**8)
from __pypy__ import builders

class Fastio:
    def __init__(self):
        self.ibuf = bytes()
        self.pil = 0
        self.pir = 0
        self.sb = builders.StringBuilder()
    def load(self):
        self.ibuf = self.ibuf[self.pil:]
        self.ibuf += read(0, 131072)
        self.pil = 0
        self.pir = len(self.ibuf)
    def flush(self): write(1, self.sb.build().encode())
    def fastin(self):
        if self.pir - self.pil < 64: self.load()
        minus = 0
        x = 0
        while self.ibuf[self.pil] < 45: self.pil += 1
        if self.ibuf[self.pil] == 45:
            minus = 1
            self.pil += 1
        while self.ibuf[self.pil] >= 48:
            x = x * 10 + (self.ibuf[self.pil] & 15)
            self.pil += 1
        if minus: return -x
        return x
    def fastout(self, x): self.sb.append(str(x))
    def fastoutln(self, x):
        self.sb.append(str(x))
        self.sb.append('\n')
fastio = Fastio()
rd = fastio.fastin
wt = fastio.fastout
wtn = fastio.fastoutln
flush = fastio.flush
register(fastio.flush)
sys.stdin, sys.stdout = None, None

rngx = 2463534242
def rng():
    global rngx
    rngx ^= rngx<<13&0xFFFFFFFF
    rngx ^= rngx>>17&0xFFFFFFFF
    rngx ^= rngx<<5&0xFFFFFFFF
    return rngx&0xFFFFFFFF

class LazyReversibleTreap:
    @staticmethod
    def make_tree(): return None

    @staticmethod
    def count(t): return t.cnt if t else 0

    def size(self, t): return self.count(t)

    def merge(self, l, r):
        if not l or not r: return l if l else r
        root = None
        leaf = None
        pos = 0
        q = []
        while l and r:
            if l.pr >= r.pr:
                self.push(l)
                if pos == 0: root = l
                elif pos == 1: leaf.r = l
                else: leaf.l = l
                leaf = l
                l = l.r
                pos = 1
            else:
                self.push(r)
                if pos == 0: root = r
                elif pos == 1: leaf.r = r
                else: leaf.l = r
                leaf = r                
                r = r.l
                pos = -1
            q.append(leaf)
        if r: leaf.r = r
        if l: leaf.l = l
        while q: self.update(q.pop())
        return self.update(root)
        
    def split(self, t, k):
        if not t: return None, None
        self.push(t)
        if k <= self.count(t.l):
            s1, s2 = self.split(t.l, k)
            t.l = s2
            return s1, self.update(t)
        else:
            s1, s2 = self.split(t.r, k - self.count(t.l) - 1)
            t.r = s1
            return self.update(t), s2
        
    def build(self, v):
        n = len(v)
        ps = [LazyReversibleTreapNode(e) for e in v]
        p = [-1] * n
        st = []
        for i in range(n):
            prv = -1
            while st and ps[i].pr > ps[st[-1]].pr:
                prv = st.pop()
            if prv != -1: p[prv] = i
            if st: p[i] = st[-1]
            st.append(i)
        root = -1
        for i in range(n):
            if p[i] != -1:
                if i < p[i]:
                    ps[p[i]].l = ps[i]
                else:
                    ps[p[i]].r = ps[i]
            else:
                root = i
        self.dfs(ps[root])
        return ps[root]
    
    def dfs(self, t):
        from collections import defaultdict
        q = [t]
        route = []
        used = defaultdict(int)
        while q:
            node = q.pop()
            if used[node]: continue
            used[node] = 1
            route.append(node)
            if node.l: q.append(node.l)
            if node.r: q.append(node.r)
        for node in route[::-1]:
            self.update(node)

    def insert(self, t, k, e):
        x1, x2 = self.split(t, k)
        return self.merge(self.merge(x1, LazyReversibleTreapNode(e)), x2)
    
    def erase(self, t, k):
        x1, x2 = self.split(t, k)
        return self.merge(x1, self.split(x2, 1)[1])
    
    @staticmethod
    def new(e): return LazyReversibleTreapNode(e)

    @staticmethod
    def toggle(t):
        if not t: return
        t.l, t.r = t.r, t.l
        t.sum = ts(t.sum)
        t.rev ^= 1
    
    @staticmethod
    def sum(t): return t.sum if t else node_e

    @staticmethod
    def propagate(t, F):
        if not t: return
        t.lazy = composition(t.lazy, F)
        t.key = mapping(t.key, F)
        t.sum = mapping(t.sum, F)

    def fold(self, t, a, b):
        x1, x2 = self.split(t, a)
        y1, y2 = self.split(x2, b-a)
        return self.sum(y1), self.merge(x1, self.merge(y1, y2))
    
    def reverse(self, t, a, b):
        x1, x2 = self.split(t, a)
        y1, y2 = self.split(x2, b-a)
        self.toggle(y1)
        return self.merge(x1, self.merge(y1, y2))

    def apply(self, t, a, b, F):
        x1, x2 = self.split(t, a)
        y1, y2 = self.split(x2, b-a)
        self.propagate(y1, F)
        return self.merge(x1, self.merge(y1, y2))
    
    def update(self, t):
        if not t: return
        self.push(t)
        t.cnt = 1
        t.sum = t.key
        if t.l:
            t.cnt += t.l.cnt
            t.sum = op(t.l.sum, t.sum)
        if t.r:
            t.cnt += t.r.cnt
            t.sum = op(t.sum, t.r.sum)
        return t
    
    def push(self, t):
        if t.rev:
            self.toggle(t.l); self.toggle(t.r)
            t.rev = 0
        if t.lazy != node_id:
            self.propagate(t.l, t.lazy); self.propagate(t.r, t.lazy)
            t.lazy = node_id
        
        
node_e = 0
node_id = 1<<30
class LazyReversibleTreapNode:
    def __init__(self, e=node_e):
        self.l = None
        self.r = None
        self.key = e
        self.sum = e
        self.lazy = node_id
        self.cnt = 1
        self.rev = 0
        self.pr = rng()

MOD = 998244353
MASK = 0x3fffffff
def op(x, y):#node1.sum * node2.sum
    a, b, c, d = x>>30, x&MASK, y>>30, y&MASK
    e = a+c; f = b+d
    if e >= MOD: e -= MOD
    if f >= MOD: f -= MOD
    return e<<30|f

def mapping(a, F):#(node.key or node.sum) * lazy ->(node.key or node.sum)
    a, b, c, d = a>>30, a&MASK, F>>30, F&MASK
    e = (c*a + d*b)%MOD; f = b
    return e<<30|f

def composition(F, G):# lazy1 * lazy2
    a, b, c, d = F>>30, F&MASK, G>>30, G&MASK
    e = a*c%MOD; f = (b*c+d)%MOD
    return e<<30|f
def ts(a): return a

filename = 'extreme_insertion_01.in'
with open(filename) as f:
    firstloop = True
    secondloop = False
    for line in f:
        if firstloop:
            firstloop = False
            secondloop = True
            N, Q = map(int,line.split())
        elif secondloop:
            secondloop = False
            A = list(map(int,line.split()))
            A = [a<<30|1 for a in A]
            rbst = LazyReversibleTreap()
            root = rbst.build(A)
        else:
            cmd, *arg = map(int, line.split())
            if cmd == 0:
                i, x = arg
                root = rbst.insert(root, i, x<<30|1)
            elif cmd == 1:
                i = arg[0]
                root = rbst.erase(root, i)
            elif cmd == 2:
                l, r = arg
                root = rbst.reverse(root, l, r)
            elif cmd == 3:
                l, r, b, c = arg
                root = rbst.apply(root, l, r, b<<30|c)
            else:
                l, r = arg
                res, root = rbst.fold(root, l, r)
                wtn(res>>30)
end = time()
wtn(end-start)

# N, Q = rd(), rd()
# A = [rd()<<30|1 for _ in range(N)]
# rbst = LazyReversibleRBST()
# root = rbst.build(A)

# for _ in range(Q):
#     cmd = rd()
#     if cmd == 0:
#         i, x = rd(), rd()
#         root = rbst.insert(root, i, x<<30|1)
#     elif cmd == 1:
#         i = rd()
#         root = rbst.erase(root, i)
#     elif cmd == 2:
#         l, r = rd(), rd()
#         root = rbst.reverse(root, l, r)
#     elif cmd == 3:
#         l, r, b, c = rd(), rd(), rd(), rd()
#         root = rbst.apply(root, l, r, b<<30|c)
#     else:
#         l, r = rd(), rd()
#         res, root = rbst.fold(root, l, r)
#         wtn(res>>30)