from pyhanlp import *
from utils import write2json, write2txt, get_time_dif, load_jieba_cut_words
import time

start_time = time.time()
words = list(HanLP.extractWords(IOUtil.newBufferedReader('36kr.txt'), 5000))
jieba_cut_words = load_jieba_cut_words('jieba_cut_words.txt')
final = [i.text for i in words if i.text not in jieba_cut_words]
write2txt('36kr_hanlp.txt', final)
time_dif = get_time_dif(start_time)
print('Time usage: %s' % time_dif)