from utils import write2txt


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
hanlp_list = load_top('36kr_hanlp.txt')
print([i for i in su_list if i not in smooth_list and not i.encode('utf-8').isalnum()])
print([i for i in su_list if i not in hanlp_list and not i.encode('utf-8').isalnum()])
su_smooth = [i for i in su_list if i not in smooth_list and not i.encode('utf-8').isalnum()]
su_hanlp = [i for i in su_list if i not in hanlp_list and not i.encode('utf-8').isalnum()]
lis = [i for i in su_smooth if i in su_hanlp]
write2txt('compare.txt', lis)