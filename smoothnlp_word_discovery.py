# -*- coding:utf-8 -*-
from smoothnlp.algorithm.phrase import extract_phrase
from utils import write2json, write2txt, get_time_dif, load_jieba_cut_words
import time

start_time = time.time()
corpus = open('36kr.txt', 'r', encoding='utf-8')
result = extract_phrase(corpus, top_k=10000, chunk_size=1000, min_n=2, max_n=4, min_freq=10)
jieba_cut_words = load_jieba_cut_words('jieba_cut_words.txt')
final = [i for i in result if i not in jieba_cut_words]
# write2json('36kr_smooth.json', result)
write2txt('36kr_smooth.txt', final)
time_dif = get_time_dif(start_time)
print('Time usage: %s' % time_dif)
