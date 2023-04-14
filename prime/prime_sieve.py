#prime_sieve O(nloglogn)
def prime_sieve(n):
    res = [1] * (n+1)
    res[0] = res[1] = 0
    for i in range(2,n):
        if i*i > n: break
        if res[i]:
            for j in range(i<<1, n+1, i): res[j] = 0
    return res
