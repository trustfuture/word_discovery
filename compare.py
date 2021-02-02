def load_top(path, topn=3000):
    with open(path, 'r') as f:
        n = 0
        result = []
        for i in f.readlines():
            if n > topn:
                break
            result.append(i.replace('\n', ''))
            n += 1
        f.close()
    return result


su_list = load_top('36kr_su.txt')
smooth_list = load_top('36kr_smooth.txt')
print([i for i in su_list if i not in smooth_list and not i.encode('utf-8').isalnum()])
print([i for i in smooth_list if i not in su_list and not i.encode('utf-8').isalnum()])