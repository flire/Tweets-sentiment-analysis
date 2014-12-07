__author__ = 'flire'
import subprocess
import sys
from tweetsParser import Tweet
from optparse import OptionParser
class StupidLemmatizer:
    def parse(self, string):
        return string
def lemmatize(tweetspath, count = float("inf"),  mystempath="./mystem"):
    outfile = tweetspath+".lemmas"
    mystem = subprocess.Popen([mystempath, "-l", "-", outfile], stdin=subprocess.PIPE, universal_newlines=True)
    lemmatizer = StupidLemmatizer()
    nextTweetNumber = 1
    with open(tweetspath, 'r') as tweetfile:
        for tweetline in tweetfile:
            tweet = Tweet(tweetline, "undef", lemmatizer)
            mystem.stdin.write(tweet.lemmatized+"\n")
            nextTweetNumber+=1
            if nextTweetNumber>count:
                break
    mystem.stdin.close()
    mystem.wait()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--count", type='int', dest="count", default=float("inf"))
    parser.add_option("--mystempath", dest="mystempath", default="./mystem")
    parser.add_option("-f", "--filename", dest="tweets_filename")
    (options, args) = parser.parse_args()
    lemmatize(options.tweets_filename, options.count, options.mystempath)
