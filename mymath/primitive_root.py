from random import randint
# my module
from prime.fast_factorize import factorize
# my module
def primitive_root(P: int) -> int:
    'primitive root of P'
    if P == 2: return 1
    ps = factorize(P-1).keys()
    while 1:
        a = randint(2, P-1)
        f = 1
        for p in ps:
            if pow(a, (P-1)//p, P) == 1:
                f = 0
                break
        if f: return a
