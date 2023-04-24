def sum_of_floor(n: int, m: int, a: int, b: int) -> int:
    'sum of floor((a * i + b)/m) for i in range(n)'
    res = 0
    if a >= m:
        q, r = divmod(a, m)
        res += (n - 1) * n * q>> 1
        a = r
    if b >= m:
        q, r = divmod(b, m)
        res += n * q
        b = r
    y = (a * n + b) // m
    if y == 0: return res
    x = y * m - b
    res += (n - (x + a - 1) // a) * y
    res += sum_of_floor(y, a, m, (a - x % a) % a)
    return res

def mod_affine_range_counting(a: int, b: int, m: int, xr: int, yr: int) -> int:
    return sum_of_floor(xr, m, a, b + m) - sum_of_floor(xr, m, a, b + m - yr)