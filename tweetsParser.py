#! /usr/bin/env python3
__author__ = 'flire'
import re
import pexpect


class Tweet:
    def __init__(self, tweetline, sentiment, lemmatized = None):
        self.author, self.tweetline = tweetline.split('\t')
        self.tweetline = self.tweetline.strip()
        self.tweetline = re.sub(r"\\(n|t)", "", self.tweetline)
        if lemmatized != None:
            self.lemmatized = lemmatized
        self.sentiment = sentiment

    def preprocess(self, url_label="", hashtag_label="", mention_label=""):
        result = re.sub('https?://[^ ]+', url_label, self.tweetline)#URL
        result = re.sub('#[^ ]+', hashtag_label, result)#hashtag
        result = re.sub('@[^ ]+', mention_label, result)#username
        return result

class LemmaExtracter:
    def __init__(self, filename):
        self.filename = filename
        self.lemma_regexp = re.compile(r"{([^}]+)}")

    def __enter__(self):
        self.file = open(self.filename, 'r')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def nextlemmas(self):
        lemmas_string = self.file.readline()
        lemmas = self.lemma_regexp.findall(lemmas_string)
        result = []
        for lemma in lemmas:
            result.append(lemma.split('|')[0])
        return result

# class TweetParser:
#     def __init__(self, mystempath):
#         self.mystem = pexpect.spawn(mystempath+" -l")
#         self.mystem.delaybeforesend = 0.1
#         self.lemma_regexp = re.compile(r"{([^}]+)}")
#
#     def __enter__(self):
#         return self
#
#     def parse(self, preprocessed_string):
#         self.mystem.flush()
#         self.mystem.sendline(preprocessed_string.encode())
#         self.mystem.expect("({.+})+")
#         lemmas_string = self.mystem.after.decode()
#         lemmas = self.lemma_regexp.findall(lemmas_string)
#         result = []
#         for lemma in lemmas:
#             result.append(lemma.split('|')[0])
#         return result
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.mystem.terminate()

def tweetsParser(filename, sentiment, total=float("inf"), skip_first=0):
    nextTweetNumber = 1
    with open(filename) as tweets:
        for i in range(skip_first):
            tweets.__next__()
        with LemmaExtracter(filename+".lemmas") as extracter:
            for tweetline in tweets:
                yield Tweet(tweetline, sentiment, extracter.nextlemmas())
                nextTweetNumber+=1
                if nextTweetNumber>total:
                    break