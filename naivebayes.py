#! /usr/bin/env python3
__author__ = 'flire'

import sys
import numpy
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from optparse import OptionParser
from tweetsParser import *


def extract_features(filename, sentiment, count):
    # result = []
    # for tweet in tweetsParser(filename, sentiment, count):
    #     result += [' '.join(tweet.lemmatized)]  # вот тут хардкод
    # return result
    for tweet in tweetsParser(filename, sentiment, count):
        yield " ".join(tweet.lemmatized)


def main(pos_tweets_filename, neg_tweets_filename, tweets_count=float("inf"), pos_label="pos",
         neg_label="neg", chunk_size = 10000, features_used=(1,1)):
    machine = BernoulliNB()
    vectorizer = HashingVectorizer(ngram_range=features_used)
    chunk_features = []
    # pos_features = extract_features(pos_tweets_filename, pos_label, tweets_count)
    # neg_features = extract_features(neg_tweets_filename, neg_label, tweets_count)
    # features = vectorizer.fit_transform(pos_features + neg_features)
    # labels = [pos_label, ] * len(pos_features) + [neg_label,] * len(neg_features)
    # machine.fit(features, labels)
    # return (machine, vectorizer, features.toarray())
    for pos_features in extract_features(pos_tweets_filename, pos_label, tweets_count):
        chunk_features.append(pos_features)
        if len(chunk_features) >= chunk_size:
            features = vectorizer.fit_transform(chunk_features)
            machine.partial_fit(features, [pos_label, ]*len(chunk_features), classes=[pos_label, neg_label])
            chunk_features = []

    if len(chunk_features)!=0:
        features = vectorizer.fit_transform(chunk_features)
        machine.partial_fit(features, [pos_label, ]*len(chunk_features), classes=[pos_label, neg_label])
        chunk_features = []


    for neg_features in extract_features(neg_tweets_filename, neg_label, tweets_count):
        chunk_features.append(neg_features)
        if len(chunk_features) >= chunk_size:
            features = vectorizer.fit_transform(chunk_features)
            machine.partial_fit(features, [neg_label, ]*len(chunk_features), classes=[pos_label, neg_label])
            chunk_features = []

    if len(chunk_features)!=0:
        features = vectorizer.fit_transform(chunk_features)
        machine.partial_fit(features, [neg_label, ]*len(chunk_features), classes=[pos_label, neg_label])
        chunk_features = []

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
        # print(res)
        if res == label:
            matched+=1
    return (len(result), matched)

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
    parser.add_option("--mystempath", dest="mystempath", default="./mystem")
    parser.add_option("-p", "--postweets", dest="postweetsfilename")
    parser.add_option("-n", "--negtweets", dest="negtweetsfilename")
    parser.add_option("--checkpos", dest="checkposfilename")
    parser.add_option("--checkneg", dest="checknegfilename")
    parser.add_option("--chunksize", type='int', dest = "chunksize", default=10000)
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
                               chunk_size=options.chunksize,
                               features_used=features_used)
    print("checking pos...")
    allpos, matchpos = count_preciseness(machine, vectorizer, options.checkposfilename, "pos")
    print("checking neg...")
    allneg, matchneg = count_preciseness(machine, vectorizer, options.checknegfilename, "neg")
    print(matchpos , '/', allpos)
    print(matchneg , '/', allneg)
    print((matchpos + matchneg) / (allpos + allneg))
    # for tweet in tweetsParser(options.postweetsfilename, "undef", 10):
    #     line = " ".join(tweet.lemmatized)
    #     tr = vectorizer.transform([line,])
    #     print(line + " -> " + str(machine.predict(tr)) + "\n")
    # for tweet in tweetsParser(options.negtweetsfilename, "undef", 10):
    #     line = " ".join(tweet.lemmatized)
    #     tr = vectorizer.transform([line,])
    #     print(line + " -> " + str(machine.predict(tr)) + "\n")
