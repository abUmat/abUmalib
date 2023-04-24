def divisors(n: int):
    'divisors of n (sorted)'
    lower , upper = [], []
    for i in range(1, n+1):
        if i*i > n: break
        if n % i == 0:
            lower.append(i)
            if i != n//i: upper.append(n//i)
    return lower + upper[::-1]
