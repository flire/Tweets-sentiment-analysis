#! /usr/bin/env python3
__author__ = 'flire'

import sys
import numpy
import scipy
from sklearn.naive_bayes import BernoulliNB
from optparse import OptionParser
from tweetsParser import *

def teach(machine, filename, sentiment, mystempath, count):
    for tweet in tweetsParser(filename, sentiment, mystempath, count):
        unigrams = tweet.lemmatized #вот тут хардкод
        print(unigrams)
        features = numpy.array(unigrams)
        labels = numpy.array([sentiment,]*len(unigrams))
        machine.partial_fit(features, labels)

def main(pos_tweets_filename, neg_tweets_filename, tweets_count=float("inf"), mystempath = "./mystem",
         pos_label="pos", neg_label="neg"):
    machine = BernoulliNB()
    teach(machine, pos_tweets_filename, pos_label, mystempath, tweets_count)
    teach(machine, neg_tweets_filename, neg_label, mystempath, tweets_count)
    return machine

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-c", "--count",type='int',dest="count", default=float("inf"))
    parser.add_option("--mystempath",dest="mystempath", default="./mystem")
    parser.add_option("-p", "--postweets",dest="postweetsfilename")
    parser.add_option("-n", "--negtweets",dest="negtweetsfilename")
    (options, args) = parser.parse_args()
    machine = main(options.postweetsfilename,
                         options.negtweetsfilename,
                         options.count,
                         options.mystempath)
    for tweet in tweetsParser(options.postweetsfilename, "undef", options.mystempath, 10):
        for unigram in tweet.lemmatized:
            sys.stdout.write(unigram + " -> " + machine.predict(unigram) + "\n")
    for tweet in tweetsParser(options.negtweetsfilename, "undef", options.mystempath, 10):
        for unigram in tweet.lemmatized:
            sys.stdout.write(unigram + " -> " + machine.predict(unigram) + "\n")
