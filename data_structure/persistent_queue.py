class PersistentQueue:
    class Node:
        def __init__(self, d, val, n) -> None:
            self.d = d
            self.val = val
            self.par = n

    def __init__(self, e) -> None:
        root = self.root = self.Node(0, e, [])
        self.start = [root]
        self.end = [root]

    def push(self, val, id_=-1):
        s = self.start[id_]; e = self.end[id_]
        ne = self.Node(e.d + 1, val, [e])
        self.start.append(s); self.end.append(ne)
        for i in range(0x100000):
            if len(e.par) <= i: break
            e = e.par[i]
            ne.par.append(e)
        return len(self.start) - 1

    def pop(self, id_=-1):
        s = self.start[id_]; e = self.end[id_]
        ns = e
        x = e.d - s.d - 1
        ds = []
        for i in range(x.bit_length()):
            if x>>i & 1: ns = ns.par[i]
        self.start.append(ns); self.end.append(e)
        return ns.val, len(self.start) - 1