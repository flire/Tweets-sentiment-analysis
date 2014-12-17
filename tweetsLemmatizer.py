#!/usr/bin/env python3
__author__ = 'flire'
import subprocess
from tweetsParser import Tweet
from optparse import OptionParser
def lemmatize(tweetspath, count = float("inf"),  mystempath="./mystem"):
    outfile = tweetspath+".preprocessed"
    nextTweetNumber = 1
    with open(tweetspath, 'r') as tweetfile:
        with open(outfile, "w") as out:
            for tweetline in tweetfile:
                tweet = Tweet(tweetline, "undef")
                out.write(tweet.preprocess()+"\n")
                nextTweetNumber+=1
                if nextTweetNumber % 10000 == 0:
                    print(nextTweetNumber)
                if nextTweetNumber>count:
                    break
    subprocess.call([mystempath, "-cl", outfile, tweetspath+".lemmas"])

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--count", type='int', dest="count", default=float("inf"))
    parser.add_option("--mystempath", dest="mystempath", default="./mystem")
    parser.add_option("-f", "--filename", dest="tweets_filename")
    (options, args) = parser.parse_args()
    lemmatize(options.tweets_filename, options.count, options.mystempath)
