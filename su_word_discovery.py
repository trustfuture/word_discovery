# -*- coding:utf-8 -*-
from config import Config
import re
from collections import Counter
import numpy as np
from tqdm import tqdm
import time
import json
from utils import write2json, write2txt, get_time_dif, load_jieba_cut_words
import time


class WordDiscovery(object):
    def __init__(self, config):
        self.n = config.n
        self.min_freq = config.min_freq
        self.min_prob = config.min_prob
        self.corpus_path = config.corpus_path
        self.lang = config.lang

    def load_corpus(self):
        '''
        读取语料
        :return:
        '''
        with open(self.corpus_path, 'r') as f:
            lines = f.readlines()
            if len(lines) == 1:
                corpus = lines[0]
            else:
                corpus = ','.join(lines)
            f.close()
        if self.lang == 'Chinese':
            corpus = re.split(u'[^\u4e00-\u9fa50-9a-zA-Z]+', corpus)  # 去掉非中文、非英文、非数字字符
        else:
            corpus = re.split(u'[^\u4e00-\u9fa50-9a-zA-Z -]+', corpus)  # 去掉非中文、非英文、非数字、非空格、非-字符，非'字符
        print('Total %d text...' % len(corpus))
        return corpus

    def generate_text(self, corpus):
        '''
        单句语料迭代器
        :param corpus:
        :return:
        '''
        for text in corpus:
            yield text

    def generate_text_ngrams(self, text):
        '''
        计算单句语料ngrams 词频
        :param text:
        :return:
        '''
        text_ngrams_count = Counter({})
        for i in range(len(text)):
            for j in range(1, self.n + 1):
                if i + j <= len(text):
                    text_ngrams_count[text[i: i + j]] += 1
        return text_ngrams_count

    def generate_corpus_ngrams(self):
        '''
        计算整个语料ngrams词频
        :return:
        '''
        corpus_ngrams_count = Counter({})
        corpus = self.load_corpus()
        print('第一步：统计阶段 开始统计ngrams词频，并按内部凝聚度筛选ngrams...')
        text_iter = self.generate_text(corpus)
        for text in tqdm(text_iter):
            text_ngrams_count = self.generate_text_ngrams(text)
            corpus_ngrams_count.update(text_ngrams_count)
        return {i: j for i, j in dict(corpus_ngrams_count).items() if j >= self.min_freq}

    def filter_ngrams(self, ngrams):
        '''
        根据内部凝聚度筛选可能成词的ngrams
        :param ngrams:
        :return:
        '''
        total = 1. * sum([j for i, j in ngrams.items() if len(i) == 1])

        def is_keep(s, ngrams):
            if len(s) >= 2:
                score = min([total * ngrams[s] / (ngrams[s[:i + 1]] * ngrams[s[i + 1:]]) for i in range(len(s) - 1)])
                return score
            else:
                return 0

        return {i: is_keep(i, ngrams) for i, j in ngrams.items() if is_keep(i, ngrams) >= self.min_prob[len(i)]}

    def split_text(self, text, ngrams):
        '''
        按筛选后的ngrams切分单句， 并统计词频
        :param text:
        :param ngrams:
        :return:
        '''
        def cut(s):
            r = np.array([0] * (len(s) - 1))
            for i in range(len(s) - 1):
                for j in range(2, self.n + 1):
                    if s[i:i + j] in ngrams:
                        r[i:i + j - 1] += 1
            w = [s[0]]
            for i in range(1, len(s)):
                if r[i - 1] > 0:
                    w[-1] += s[i]
                else:
                    w.append(s[i])
            return w
        words = Counter({})
        for i in cut(text):
            words[i] += 1
        return words

    def split_corpus(self, ngrams):
        '''
        按筛选后的ngrams切分整个语料，并统计词频
        :param ngrams:
        :return:
        '''
        corpus_words_count = Counter({})
        corpus = self.load_corpus()
        print('第二步：切分阶段 按筛选后的ngrams切分整个语料，并统计词频...')
        for text in tqdm(corpus):
            if text:
                corpus_words_count.update(self.split_text(text, ngrams))
        return corpus_words_count

    # 回溯
    def recall(self, corpus_words_count, ngrams):
        '''
        回溯，检查大于3的词的每个片段在不在ngrams中，有一个不在就出局
        :param corpus_words_count:
        :param ngrams:
        :return:
        '''
        def is_real(s, ngrams):
            if len(s) >= 3:
                for i in range(3, self.n + 1):
                    for j in range(len(s) - i + 1):
                        if s[j:j + i] not in ngrams:
                            return False
                return True
            else:
                return True
        print('第三阶段：回溯 检查大于3的词的每个片段在不在ngrams中，有一个不在就出局...')
        result = {i: j for i, j in corpus_words_count.items() if is_real(i, ngrams)}
        return result

if __name__ == '__main__':
    corpus_path = './36kr.txt'
    config = Config(corpus_path)
    w = WordDiscovery(config)

    start_time = time.time()
    corpus_ngrams = w.generate_corpus_ngrams()
    filtered_ngrams = w.filter_ngrams(corpus_ngrams)
    corpus_words_count = w.split_corpus(filtered_ngrams)
    result = w.recall(corpus_words_count, filtered_ngrams)
    jieba_cut_words = load_jieba_cut_words('jieba_cut_words.txt')

    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    print(result)
    # result_score = {i: filtered_ngrams.get(i) for i, _ in result.items() if i in filtered_ngrams}
    # result_score = dict(sorted(result_score.items(), key=lambda item: item[1], reverse=True))
    # # write2json('36kr_su.json', {i: j for i, j in result.items() if len(i) >= 2})
    # final = [i for i, j in result_score.items() if len(i) >= 2 and i not in jieba_cut_words]
    # write2txt('36kr_su.txt', final)
    # time_dif = get_time_dif(start_time)
    # print('Time usage: %s' % time_dif)



    # with open('36kr_result.json', 'w', encoding='utf-8') as f:
    #     data_json = json.dumps({i: j for i, j in result.items() if len(i) >= 2}, ensure_ascii=False)
    #     f.write(data_json)
    #     f.close()

