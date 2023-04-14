def LIS(A, non_decreasing=False):
    if non_decreasing:
        from bisect import bisect_right as bis
    else:
        from bisect import bisect_left as bis
    N = len(A)
    dp = []
    res = [None] * N
    for i in range(N):
        a = A[i]
        j = bis(dp, a)
        if j == len(dp):
            dp.append(a)
        else:
            dp[j] = a
        res[i] = j
    ind, val = [], []
    j = len(dp)-1
    for i in range(N-1, -1, -1):
        if res[i] == j:
            ind.append(i)
            val.append(A[i])
            j -= 1
    return len(dp), ind[::-1], val[::-1]
