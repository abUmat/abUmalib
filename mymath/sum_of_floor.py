# https://nyaannyaan.github.io/library/math/sum-of-floor.hpp
def sum_of_floor(n: int, m: int, a: int, b: int) -> int:
    'sum of floor((a * i + b)/m) for i in range(n)'
    res = 0
    if a >= m:
        quo, a = divmod(a, m)
        res += (n - 1) * n * quo >> 1
    if b >= m:
        quo, b = divmod(b, m)
        res += n * quo
    y = (a * n + b) // m
    if y == 0: return res
    x = y * m - b
    res += (n - (x + a - 1) // a) * y
    res += sum_of_floor(y, a, m, -x % a)
    return res

def mod_affine_range_counting(a: int, b: int, m: int, xr: int, yr: int) -> int:
    return sum_of_floor(xr, m, a, b + m) - sum_of_floor(xr, m, a, b + m - yr)
