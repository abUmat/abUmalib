def totient(n: int) -> int:
    res = n
    for i in range(2, n + 1):
        if i * i > n: break
        if not n % i:
            res -= res //i
            while not n % i: n //= i
    if n != 1: res -= res // n
    return res