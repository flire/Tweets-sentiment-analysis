#! /usr/bin/env python3
__author__ = 'flire'
import re
import pexpect


class Tweet:
    def __init__(self, tweetline, sentiment, lemmatizer):
        self.author, self.tweetline = tweetline.split('\t')
        self.tweetline = self.tweetline.strip()
        self.tweetline = re.sub(r"\\(n|t)", "", self.tweetline)
        self.lemmatized = lemmatizer.parse(self.preprocess())
        self.sentiment = sentiment

    def preprocess(self, url_label="", hashtag_label="", mention_label=""):
        result = re.sub('https?://[^ ]+', url_label, self.tweetline)#URL
        result = re.sub('#[^ ]+', hashtag_label, result)#hashtag
        result = re.sub('@[^ ]+', mention_label, result)#username
        return result


class TweetParser:
    def __init__(self, mystempath):
        self.mystem = pexpect.spawn(mystempath+" -l")
        self.mystem.delaybeforesend = 0.1
        self.lemma_regexp = re.compile(r"{([^}]+)}")

    def __enter__(self):
        return self

    def parse(self, preprocessed_string):
        self.mystem.flush()
        self.mystem.sendline(preprocessed_string.encode())
        self.mystem.expect("({.+})+")
        lemmas_string = self.mystem.after.decode()
        lemmas = self.lemma_regexp.findall(lemmas_string)
        result = []
        for lemma in lemmas:
            result.append(lemma.split('|')[0])
        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mystem.terminate()

def tweetsParser(filename, sentiment, mystem_path="./mystem", total=float("inf")):
    file = open(filename, 'r')
    nextTweetNumber = 1
    with TweetParser(mystem_path) as parser:
        for tweetline in file:
            yield Tweet(tweetline, sentiment, parser)
            nextTweetNumber+=1
            if nextTweetNumber>total:
                break
    file.close()
