def number_of_subsequences(s: "Iterable", empty: bool=False, mod: int=0) -> int:
    '''
    s: iterable
    empty: if True, include empty string
    mod: mod
    '''
    # 微妙な応用問題が出題されそうなのでメモ
    # https://atcoder.jp/contests/abc214/editorial/2440?lang=ja
    # 以下の説明は1-indexed
    # dp[i] := sの1文字目からi文字目までのsubsequenceのうち, s[i]を使うもの
    # dp[0] := 1(空文字列)
    # k := s[i] == s[k] && k < i を満たす最大の整数(存在しない場合k = 0)とすると
    # dp[i] = sum{dp[j] for j in [k, i)}
    # これを実装すると...
    # n = len(s)
    # compress = {a: i for i, a in enumerate(sorted(set(s)))} # 座圧
    # s = [compress[a] for a in s] # 座圧後配列
    # idx = [0] * len(compress) # idx[c] := i(iは s[i] == c を満たす最大の整数)
    # cum = [0] * (n + 2) # 累積和
    # cum[0] = 0; cum[1] = 1
    # for i in range(n):
    #     char = s[i]
    #     k = idx[char]
    #     dp = cum[i + 1] - cum[k]
    #     idx[char] = i + 1
    #     cum[i + 2] = (cum[i + 1] + dp) % mod
    # return cum[-1]

    # 高速化
    # ep[i] := sum{dp[j] for j in [0, i]}とすると
    # ep[i] = dp[i] + ep[i - 1]
    #       = sum{dp[j] for j in [k, i)} + ep[i - 1]
    #       = (ep[i - 1] - ep[k - 1]) + ep[i - 1]
    # ep_dict[c] := ep[i](iは s[i] == c を満たす最大の整数)
    ep_dict = {}
    ep = 1 # ep[0]
    for c in s:
        tmp = ep_dict.get(c, 0) # tmp = ep[k - 1]
        ep_dict[c] = ep # ep_dict[c]の更新
        ep = (ep << 1) - tmp # ep[i] = ep[i - 1] * 2 - ep[k - 1]
        if ep < 0: ep += mod
        elif ep >= mod: ep -= mod
    if not empty: ep -= 1
    if ep < 0: ep += mod
    return ep