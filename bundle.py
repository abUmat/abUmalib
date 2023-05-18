from collections import deque, defaultdict
import sys

if __name__ == '__main__':
    q = deque([sys.argv[1] + '.py'])
    G = defaultdict(set)
    G[sys.argv[1] + '.py'] = set()
    deg = defaultdict(int)
    while q:
        file = q.popleft()
        bundle_flag = 0
        with open(file) as f:
            for line in f:
                if line[:11] == '# my module':
                    if bundle_flag:
                        bundle_flag = 0
                        break
                    else:
                        bundle_flag = 1
                elif bundle_flag:
                    path = '/'.join(line.split()[1].split('.')) + '.py'
                    if file not in G[path]:
                        G[path].add(file)
                        q.append(path)
                        deg[file] += 1
    q = [k for k in G.keys() if not deg[k]]
    res = []
    for file in q:
        bundle_flag = 0
        with open(file) as f:
            for line in f:
                if line[:11] == '# my module':
                    if bundle_flag:
                        bundle_flag = 0
                    else:
                        bundle_flag = 1
                elif not bundle_flag:
                    res.append(line)
        for ff in G[file]:
            deg[ff] -= 1
            if deg[ff] == 0:
                q.append(ff)
        res.append('\n')

    output_file = sys.argv[2] + '.py'
    with open(output_file, mode='w') as f:
        f.writelines(res)
