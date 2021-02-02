# -*- coding:utf-8 -*-
import json
import time
from datetime import timedelta


def write2json(path, data: dict):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()


def write2txt(path, data: list):
    with open(path, 'w', encoding='utf-8') as f:
        for i in data:
            f.write(i + '\n')
        f.close()


def load_jieba_cut_words(path):
    words = []
    with open(path, 'r') as f:
        for word in f.readlines():
            words.append(word.replace('\n', ''))
    return set(words)


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))
