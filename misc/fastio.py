from atexit import register
from os import read, write
import sys
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
def rdl(n): return [rd() for _ in range(n)]
wt = fastio.fastout
wtn = fastio.fastoutln
def wtnl(l): wtn(' '.join(map(str, l)))
flush = fastio.flush
register(flush)
sys.stdin, sys.stdout = None, None
