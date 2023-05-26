# my module
from mymath.gcd_lcm import *
from mymath.modinv import *
# my module
# https://nyaannyaan.github.io/library/modulo/mod-log.hpp
def mod_log(a: int, b: int, p: int) -> int:
    'return k s.t. a**k == y (mod p) if exist, else -1'
    if a % p < 0: a = a % p + p
    if b % p < 0: b = b % p + p
    r = 1 % p
    for f in range(10**8):
        g = gcd2(a, p)
        if g == 1: break
        if b % g: return f if r == b else -1
        b //= g
        p //= g
        r = r * (a // g) % p
    if p == 1: return f
    ir = modinv(r, p)
    b = b * ir  % p
    ak = 1
    baby = {}
    for k in range(p + 1):
        if k * k >= p: break
        if ak not in baby.keys(): baby[ak] = k
        ak = ak * a % p
    iak = modinv(ak, p)
    for i in range(k):
        if b in baby.keys(): return f + i * k + baby[b]
        b = b * iak % p
    return -1
