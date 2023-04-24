def kth_root_integer(a: int, k: int) -> int:
    'floor(a ** (1/k))'
    if a <= 1 or k == 1: return a
    if 64 <= k: return 1
    def check(n: int) -> bool:
        x = 1; m = n
        p = k
        while p:
            if p & 1: x *= m
            p >>= 1
            m *= m
        return x <= a
    n = int(pow(a, 1 / k))
    while not check(n): n -= 1
    while check(n + 1): n += 1
    return n
