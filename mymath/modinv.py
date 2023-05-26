def modinv(a: int, m: int) -> int:
    '''mod mでのaの逆元を求める'''
    b = m; u = 1; v = 0
    while b:
        t = a // b
        a, b = b, a - t * b
        u, v = v, u - t * v
    u %= m
    return u