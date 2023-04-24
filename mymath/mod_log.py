# my module
from mymath.gcd_lcm import *
# my module
def mod_log(a: int, b: int, p: int) -> int:
    'return k s.t. a**k == y (mod p) if exist, else -1'
    def inv(a: int, p: int) -> int:
        b = p; x = 1; y = 0
        while a:
            q = b // a
            a, b = b % a, a
            x, y = y - q * x, x
        return y + p if y < 0 else y
    if a % p < 0: a = a % p + p
    if b % p < 0: b = b % p + p
    r = 1 % p
    for f in range(10**8):
        g = gcd(a, p)
        if g == 1: break
        if b % g: return f if r == b else -1
        b //= g
        p //= g
        r = r * (a // g) % p
    if p == 1: return f
    ir = inv(r, p)
    b = b * ir  % p
    ak = 1
    baby = {}
    for k in range(p + 1):
        if k * k >= p: break
        if ak not in baby.keys(): baby[ak] = k
        ak = ak * a % p
    iak = inv(ak, p)
    for i in range(k):
        if b in baby.keys(): return f + i * k + baby[b]
        b = b * iak % p
    return -1