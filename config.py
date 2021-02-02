# -*- coding:utf-8 -*-

class Config(object):
    def __init__(self, corpus_path):
        self.n = 4
        self.min_freq = 10
        self.corpus_path = corpus_path
        self.lang = 'Chinese'
        self.min_prob = {1: 1, 2: 5, 3: 25, 4: 125}
