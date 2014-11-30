#! /usr/bin/env python3
__author__ = 'flire'

import sys
from optparse import OptionParser
from tweetsParser import *
import operator

def compose_dictionary(filename, sentiment, path, count, dictsize):
    freqs = {}
    for tweet in tweetsParser(filename, options.sentiment, options.mystempath, options.count):
        unigrams = tweet.lemmatized
        print(unigrams)
        for word in unigrams:
            freq = freqs.get(word, None)
            if freq == None:
                freqs[word] = 1
            else:
                freqs[word] = freq + 1
    sorted_freqs = sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
    if dictsize !=0:
        return sorted_freqs[:dictsize]
    else:
        return sorted_freqs

def intersect_dicts(positive_dict, negative_dict, pos_label="pos", neg_label="neg"):
    result = {}
    pos_keys = set(positive_dict.keys())
    neg_keys = set(negative_dict.keys())
    intersection = pos_keys & neg_keys
    for pos_key in pos_keys - intersection:
        result[pos_key] = pos_label
    for neg_key in neg_keys - intersection:
        result[neg_key] = neg_label


if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-s", "--sentiment", dest="sentiment", default="pos")
    parser.add_option("-c", "--count",type='int',dest="count", default=float("inf"))
    parser.add_option("--dictsize",dest="dictsize",type='int', default=0)
    parser.add_option("--mystempath",dest="mystempath", default="./mystem")
    parser.add_option("-f", "--filename",dest="filename")
    (options, args) = parser.parse_args()
    unigrams_dict = compose_dictionary(options.filename, options.sentiment, options.mystempath, options.count, options.dictsize)
    sys.stdout.write(str(unigrams_dict))
