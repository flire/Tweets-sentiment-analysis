#! /usr/bin/env python3
__author__ = 'flire'

import sys
import numpy
from sklearn.naive_bayes import BernoulliNB
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from optparse import OptionParser
from tweetsParser import *


def extract_features(filename, sentiment, count):
    for tweet in tweetsParser(filename, sentiment, count):
        yield " ".join(tweet.lemmatized)


def main(pos_tweets_filename, neg_tweets_filename, tweets_count=float("inf"), pos_label="pos",
         neg_label="neg", features_used=(1,1)):
    machine = svm.SVC()
    vectorizer = CountVectorizer(ngram_range=features_used)
    pos_features_chunk = []
    for pos_features in extract_features(pos_tweets_filename, pos_label, tweets_count):
        pos_features_chunk.append(pos_features)

    neg_features_chunk = []
    for neg_features in extract_features(neg_tweets_filename, neg_label, tweets_count):
        neg_features_chunk.append(neg_features)

    features = vectorizer.fit_transform(pos_features_chunk+neg_features_chunk)
    machine.fit(features, [pos_label,]*len(pos_features_chunk) + [neg_label,]*len(neg_features_chunk))

    return (machine, vectorizer)

def count_preciseness(machine, vectorizer, source, label):
    matched = 0
    chunk = []
    for tweet in tweetsParser(source, "undef"):
        line = " ".join(tweet.lemmatized)
        chunk.append(line)
    tr = vectorizer.transform(chunk)
    result = machine.predict(tr)
    for res in result:
        if res == label:
            matched+=1
    return (len(result), matched)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--count", type='int', dest="count", default=float("inf"))
    parser.add_option("--mystempath", dest="mystempath", default="./mystem")
    parser.add_option("-p", "--postweets", dest="postweetsfilename")
    parser.add_option("-n", "--negtweets", dest="negtweetsfilename")
    parser.add_option("--checkpos", dest="checkposfilename")
    parser.add_option("--checkneg", dest="checknegfilename")
    parser.add_option("--features", dest="features", default="unigrams")
    (options, args) = parser.parse_args()
    features_used = (1,1)
    if options.features == "bigrams":
        features_used = (2,2)
    elif options.features == "unigrams_bigrams":
        features_used = (1,2)
    print("learning...")
    machine, vectorizer = main(options.postweetsfilename,
                               options.negtweetsfilename,
                               options.count,
                               pos_label="pos",
                               neg_label="neg",
                               features_used=features_used)
    print("checking pos...")
    allpos, matchpos = count_preciseness(machine, vectorizer, options.checkposfilename, "pos")
    print("checking neg...")
    allneg, matchneg = count_preciseness(machine, vectorizer, options.checknegfilename, "neg")
    print(matchpos , '/', allpos)
    print(matchneg , '/', allneg)
    print((matchpos + matchneg) / (allpos + allneg))
