def modinv(a: int, m: int) -> int:
    '''return x s.t. x == a^(-1) (mod m)'''
    b = m; u = 1; v = 0
    while b:
        t = a // b
        a, b = b, a - t * b
        u, v = v, u - t * v
    u %= m
    return u