from collections import deque, defaultdict
import sys

if __name__ == '__main__':
    TYPING_TEMPLATE = 'misc/typing_template.py'
    q1 = deque([sys.argv[1] + '.py'])
    G = defaultdict(set)
    G[sys.argv[1] + '.py'] = set()
    deg = defaultdict(int)
    while q1:
        file = q1.popleft()
        is_header = 0
        with open(file) as f:
            for line in f:
                if line[:11] == '# my module':
                    if is_header: is_header = 0; break
                    else: is_header = 1
                elif is_header:
                    path = '/'.join(line.split()[1].split('.')) + '.py'
                    if path != TYPING_TEMPLATE:
                        if file not in G[path]:
                            G[path].add(file)
                            q1.append(path)
                            deg[file] += 1
    q2 = [k for k in G.keys() if not deg[k]]
    res = deque()
    with open(TYPING_TEMPLATE) as f:
        for line in f: res.append(line)
    res.append('\n')
    for file in q2:
        is_header = 0
        with open(file) as f:
            for line in f:
                if line[:11] == '# my module':
                    if is_header: is_header = 0
                    else: is_header = 1
                elif not is_header:
                    if line[:4] == 'from' or line[:6] == 'import':
                        res.appendleft(line)
                    else:
                        res.append(line)
        for ff in G[file]:
            deg[ff] -= 1
            if deg[ff] == 0:
                q2.append(ff)
        res.append('\n')
    output_file = sys.argv[2] + '.py'
    with open(output_file, mode='w') as f:
        f.writelines(res)
