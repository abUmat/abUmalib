class SplayTreeBase:
    def __init__(self, Node, e, id_):
        self.Node = Node
        self.e = e
        self.id = id_

    def new(self, *arg): return self.Node(self.e, self.id, *arg)

    @staticmethod
    def delete(t):
        if t.l: t.l.p = None
        if t.r: t.r.p = None
        if t.p:
            if t.p.l == t: t.p.l = None
            if t.p.r == t: t.p.r = None
    @staticmethod
    def is_root(t):  return ((t.p is None) or (t.p.l != t and t.p.r != t))
    @staticmethod
    def _count(t): return t.cnt if t else 0
    @staticmethod
    def pos(t):
        if t.p:
            if t.p.l == t: return -1
            if t.p.r == t: return 1
        return 0

    def size(self, t): return self._count(t)

    def splay(self, t): #virtual
        self.push(t)
        while not ((t.p is None) or (t.p.l != t and t.p.r != t)):
            q = t.p
            if ((q.p is None) or (q.p.l != q and q.p.r != q)):
                self.push(q); self.push(t); self.rot(t)
            else:
                r = q.p
                self.push(r); self.push(q); self.push(t)
                if q.p.l == q: posq = -1
                else: posq = 1
                if t.p.l == t: post = -1
                else: post = 1
                if posq == post: self.rot(q); self.rot(t)
                else: self.rot(t); self.rot(t)

    def get_left(self, t):
        while t.l:
            self.push(t)
            t = t.l
        return t

    def get_right(self, t):
        while t.r:
            self.push(t)
            t = t.r
        return t

    def split(self, t, k):
        if not t: return None, None
        if k == 0: return None, t
        cnt = t.cnt if t else 0
        if k == cnt: return t, None
        self.push(t)
        cnt = t.l.cnt if t.l else 0
        if k <= cnt:
            x1, x2 = self.split(t.l, k)
            t.l = x2
            t.p = None
            if x2: x2.p = t
            self.update(t)
            return x1, t
        else:
            x1, x2 = self.split(t.r, k-cnt-1)
            t.r = x1
            t.p = None
            if x1: x1.p = t
            self.update(t)
            return t, x2

    def merge(self, l, r):
        if not l and not r: return None
        if not l:
            self.splay(r)
            return r
        if not r:
            self.splay(l)
            return l
        self.splay(l); self.splay(r)
        l = self.get_right(l)
        self.splay(l)
        l.r = r
        r.p = l
        self.update(l)
        return l

    def insert(self, t, k, *arg):
        self.splay(t)
        x1, x2 = self.split(t, k)
        return self.merge(self.merge(x1, self.new(*arg)), x2)

    def erase(self, t, k):
        self.splay(t)
        x1, x2 = self.split(t, k)
        y1, y2 = self.split(x2, 1)
        self.delete(y1)
        return self.merge(x1, y2)

    def build(self, v, l=0, r=0):
        if not r: r = len(v)
        if l+1 >= r: return self.new(v[l])
        return self.merge(self.build(v, l, l+r>>1), self.build(v, l+r>>1, r))

    def rot(self, t): #virtual
        x = t.p; y = x.p
        if x.l == t:
            z = t.r; x.l = z
            if z: z.p = x
            t.r = x
            x.p = t
        else:
            z = t.l; x.r = z
            if z: z.p = x
            t.l = x
            x.p = t
        self.update(x)
        self.update(t)
        t.p = y
        if y:
            if y.l == x: y.l = t
            if y.r == x: y.r = t
