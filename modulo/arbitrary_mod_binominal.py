class PrimePowerBinomial:
    def __init__(self, _p, _q):
        self.N_MAX = 20000000
        self.M_MAX = (1<<30)-1
        self.p, self.q = _p, _q
        m = 1
        while _q:
            m *= self.p
            _q -= 1
        self.M = m
        self.mask = self.M-1
        self.delta = 1 if self.p == 2 and self.q >= 3 else -1
        # 前計算
        MX = min(self.M, self.N_MAX+10)
        self.fac = [0] * MX
        self.ifac = [0] * MX
        self.inv = [0] * MX
        self.fac[0] = self.ifac[0] = self.inv[0] = 1
        self.fac[1] = self.ifac[1] = self.inv[1] = 1
        i = 2
        while i < MX:
            if i%self.p:
                self.fac[i] = self.fac[i-1] * i % self.M
            else:
                self.fac[i] = self.fac[i-1]
                self.fac[i+1] = self.fac[i-1] * (i+1) % self.M
                i += 1
            i += 1
        self.ifac[MX-1] = pow(self.fac[-1], self.M//self.p * (self.p-1) - 1, self.M)
        i = MX-2
        while i > 1:
            if i%self.p:
                self.ifac[i] = self.ifac[i+1] * (i+1) % self.M
            else:
                self.ifac[i] = self.ifac[i+1] * (i+1) % self.M
                self.ifac[i-1] = self.ifac[i]
                i -= 1
            i -= 1

    def C(self, n, m):
        if n < m or n < 0 or m < 0: return 0
        # Lucasの定理
        if self.q == 1:
            res = 1
            while n:
                n, n0 = n//self.p, n%self.p
                m, m0 = m//self.p, m%self.p
                if n0 < m0: return 0
                res = res * self.fac[n0] % self.M
                buf = self.ifac[n0-m0] * self.ifac[m0] % self.M
                res = res * buf % self.M
            return res
        r = n-m
        e0, eq, i = 0, 0, 0
        res = 1
        if self.p == 2:
            # bit演算で定数倍高速化
            while n:
                res = res * self.fac[n& self.mask] & self.mask
                res = res * self.ifac[m& self.mask] & self.mask
                res = res * self.ifac[r& self.mask] & self.mask
                n >>= 1
                m >>= 1
                r >>= 1
                eps = n-m-r
                e0 += eps
                if e0 >= self.q: return 0
                i += 1
                if i >= self.q: eq += eps
            if eq & 1: res = res  * self.delta & self.mask
            res = res * pow(self.p, e0, self.M) & self.mask
        else:
            while n:
                res = res * self.fac[n%self.M] % self.M
                res = res * self.ifac[m%self.M] % self.M
                res = res * self.ifac[r%self.M] % self.M
                n = n//self.p
                m = m//self.p
                r = r//self.p
                eps = n-m-r
                e0 += eps
                if e0 >= self.q: return 0
                i += 1
                if i >= self.q: eq += eps
            if eq & 1: res = res  * self.delta % self.M
            res = res * pow(self.p, e0, self.M) % self.M
        return res

class ArbitraryModBinomial:
    @staticmethod
    def crt(V):
        def extgcd(a, b):
            if b:
                d, y, x = extgcd(b, a % b)
                y -= (a // b) * x
                return d, x, y
            return a, 1, 0
        x = 0; d = 1
        for X, Y in V:
            g, a, b = extgcd(d, Y)
            x, d = (Y*b*x + d*a*X) // g, d*(Y // g)
            x %= d
        return x, d

    def __init__(self, mod):
        self.mod = mod
        self.M = []
        self.cs = []
        for i in range(2, mod):
            if i*i > mod: break
            if not mod%i:
                j, k = 0, 1
                while not mod%i:
                    mod //= i
                    j += 1
                    k *= i
                self.M.append(k)
                self.cs.append(PrimePowerBinomial(i, j))
        if mod != 1:
            self.M.append(mod)
            self.cs.append(PrimePowerBinomial(mod, 1))

    def __call__(self, n, m):
        if self.mod == 1: return 0
        V = []
        for i in range(len(self.cs)):
            V.append((self.cs[i].C(n, m), self.M[i]))
        return self.crt(V)[0]
