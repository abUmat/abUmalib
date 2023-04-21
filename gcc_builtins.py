def popcount(x: int):
    x = x - ((x >> 1) & 0x55555555)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = (x + (x >> 4)) & 0x0f0f0f0f
    x = x + (x >> 8)
    x = x + (x >> 16)
    return x & 0x0000007f

def popcountll(x: int):
    x = x - ((x >> 1) & 0x5555555555555555)
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f
    x = x + (x >> 8)
    x = x + (x >> 16)
    x = x + (x >> 32)
    return x & 0x0000007f

def parity(x: int):
    if x >> 32: return popcount(x) & 1
    return popcountll(x) & 1

def ffs(x: int):
    return (x & -x).bit_length()

def clz(x: int):
    return 32 - x.bit_length()

def clzll(x: int):
    return 64 - x.bit_length()

def ctz(x: int):
    return  (x & -x).bit_length() - 1
