from collections import deque
class SlideWindowAggregationDeque:
    def __init__(self, e, swagfunc):
        self.e = self.f0 = self.f1 = e
        self.swagfunc = swagfunc
        self.a0 = deque()
        self.a1 = deque()
        self.r0 = deque([e])
        self.r1 = deque([e])

    def append(self, x):
        self.a1.append(x)
        self.f1 = self.swagfunc(self.f1, x)
        self.r1.append(self.f1)

    def appendleft(self, x):
        self.a0.append(x)
        self.f0 = self.swagfunc(x, self.f0)
        self.r0.append(self.f0)

    def _transfer0to1(self):
        cnt = (len(self.a0)+1)>>1
        A = deque()
        for _ in range(cnt): A.append(self.a0.popleft())
        while A: self.append(A.pop())
        #rebuild0
        self.f0 = self.e
        self.r0 = deque([self.e])
        for a in self.a0:
            self.f0 = self.swagfunc(a, self.f0)
            self.r0.append(self.f0)

    def _transfer1to0(self):
        cnt = (len(self.a1)+1)>>1
        A = deque()
        for _ in range(cnt): A.append(self.a1.popleft())
        while A: self.appendleft(A.pop())
        #rebuild1
        self.f1 = self.e
        self.r1 = deque([self.e])
        for a in self.a1:
            self.f1 = self.swagfunc(self.f1, a)
            self.r1.append(self.f1)

    def pop(self):
        if not self.a1: self._transfer0to1()
        self.a1.pop()
        self.r1.pop()
        self.f1 = self.r1[-1]

    def popleft(self):
        if not self.a0: self._transfer1to0()
        self.a0.pop()
        self.r0.pop()
        self.f0 = self.r0[-1]

    def query(self): return self.swagfunc(self.f0, self.f1)
