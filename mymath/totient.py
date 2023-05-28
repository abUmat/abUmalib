# my module
from prime.prime_enumerate import *
# my module
def totient(n: int) -> int:
    "return: count x in [1, n) s.t. gcd(x, n) == 1"
    ps = prime_enumerate(n)
    res = n
    for p in ps:
        if p * p > n: break
        if not n % p:
            res -= res // p
            while not n % p: n //= p
    if n != 1: res -= res // n
    return res