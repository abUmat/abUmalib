# my module
from misc.typing_template import *
# my module
def divisors(n: int) -> List[int]:
    'return: divisors of n (sorted)'
    lower , upper = [], []
    for i in range(1, n+1):
        if i*i > n: break
        if n % i == 0:
            lower.append(i)
            if i != n//i: upper.append(n//i)
    return lower + upper[::-1]
