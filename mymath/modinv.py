def modinv(a: int, m: int) -> int:
    '''mod mでのaの逆元を求める'''
    b = m; u = 1; v = 0
    while b:
        t = a // b
        a -= t * b; a, b = b, a
        u -= t * v; u, v = v, u
    u %= m
    return u