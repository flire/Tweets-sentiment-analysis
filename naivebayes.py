#! /usr/bin/env python3
__author__ = 'flire'

import sys
import numpy
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from optparse import OptionParser
from tweetsParser import *


def extract_features(filename, sentiment, count, skip_first=0):
    result = []
    for tweet in tweetsParser(filename, sentiment, count, skip_first):
        result += [' '.join(tweet.lemmatized)]  # вот тут хардкод
    return result


def main(pos_tweets_filename, neg_tweets_filename, tweets_count=float("inf"), skip_first=0, pos_label="pos",
         neg_label="neg"):
    machine = BernoulliNB()
    vectorizer = CountVectorizer(ngram_range=(1,1))
    pos_features = extract_features(pos_tweets_filename, pos_label, tweets_count, skip_first)
    neg_features = extract_features(neg_tweets_filename, neg_label, tweets_count, skip_first)
    features = vectorizer.fit_transform(pos_features + neg_features)
    labels = [pos_label, ] * len(pos_features) + [neg_label,] * len(neg_features)
    machine.fit(features, labels)
    return (machine, vectorizer, features.toarray())


if __name__ == "__main__":
    # vectorizer = CountVectorizer(ngram_range=(1,2))
    # q = ['qqq www eee', 'qqq eee ttt']
    # f = vectorizer.fit_transform(q)
    # print(f)
    # print(vectorizer.get_feature_names())
    # w = ['ttt www eee zzz']
    # print(vectorizer.transform(w))
    # exit()
    parser = OptionParser()
    parser.add_option("-c", "--count", type='int', dest="count", default=float("inf"))
    parser.add_option("--skip", type='int', dest="skipfirst", default=0)
    parser.add_option("--mystempath", dest="mystempath", default="./mystem")
    parser.add_option("-p", "--postweets", dest="postweetsfilename")
    parser.add_option("-n", "--negtweets", dest="negtweetsfilename")
    (options, args) = parser.parse_args()
    machine, vectorizer, features = main(options.postweetsfilename,
                   options.negtweetsfilename,
                   options.count,
                   skip_first=options.skipfirst)
    for tweet in tweetsParser(options.postweetsfilename, "undef", options.mystempath, 10):
        line = " ".join(tweet.lemmatized)
        tr = vectorizer.transform([line,])
        print(line + " -> " + str(machine.predict(tr)) + "\n")
    for tweet in tweetsParser(options.negtweetsfilename, "undef", options.mystempath, 10):
        line = " ".join(tweet.lemmatized)
        tr = vectorizer.transform([line,])
        print(line + " -> " + str(machine.predict(tr)) + "\n")
