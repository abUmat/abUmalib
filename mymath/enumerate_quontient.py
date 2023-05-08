def fast_div(a: int, b: int) ->int: return int(a / b)
def slow_div(a: int, b: int) -> int: return a // b
def enumerate_quotient(N: int, f) -> None:
    sq = int(N ** 0.5)
    def func(d):
        upper = N
        quo = 0
        while upper > sq:
            quo += 1
            thres = d(N, quo + 1)
            f(quo, thres, upper)
            upper = thres
        while upper > 0:
            f(d(N, upper), upper - 1, upper)
            upper -= 1
    if N <= 1e12: func(fast_div)
    else: func(slow_div)