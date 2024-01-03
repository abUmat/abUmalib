def _rng():
    from random import randint
    rngx = randint(1, 100000)
    while 1:
        rngx ^= rngx<<13&0xFFFFFFFF
        rngx ^= rngx>>17&0xFFFFFFFF
        rngx ^= rngx<<5&0xFFFFFFFF
        yield rngx&0xFFFFFFFF
_rand = _rng()
def rand():
    return next(_rand)
