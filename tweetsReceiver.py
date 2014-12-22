#! /usr/bin/env python2
__author__ = 'flire'
#up to 100 tweets!!!!!!!
import twitter
import time
from optparse import OptionParser

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--count",type='int', dest="count", default=1000)
    parser.add_option("-p", type='int', dest="pausetime", default=300)
    parser.add_option("-o", dest="outfilename")
    (options, args) = parser.parse_args()

    api = twitter.Api(consumer_key='LVPLcRvqtkY4jFrI9MKFO6xmf',
                      consumer_secret='ntuCkjKVDis5VhTHDg5IzninByJ2fDk4N6k3q03Z2T4osiNU7Z',
                      access_token_key='2534734495-EKZSEFemtAyDtx0GJIxTgYjkYLhXBBwu1haJnkj',
                      access_token_secret='jUnswfP44ekZRNECYMTsrOcQPihR2nnelHeM4nFbxAaIp')
    count = 0
    total = options.count
    with open(options.outfilename,"w") as out:
        while count < total:
            number_to_get = min(total-count, 100)
            search = api.GetSearch(term=u"рубль",lang='ru', result_type='recent', count=number_to_get, max_id='')
            for tweetIndex in range(len(search)):
                tweetline = search[tweetIndex].text.encode("utf-8")
                tweetline = tweetline.translate(str.maketrans({"\n": "\\n", "\t": "\\t"}))
                print tweetline
                outline = "{0}\t{1}\n".format(search[tweetIndex].user.screen_name, tweetline)
                out.write(outline)
                # if options.header == "author":
                #     header = search[tweetIndex].user.screen_name + ":\n"
                # elif options.header == "number":
                #     header = "#" + str(tweetIndex) + ":\n"
                # elif options.header == "full":
                #     header = '#' + str(tweetIndex+1) + " by " + search[tweetIndex].user.screen_name + ':\n'
                # sys.stdout.write(header)
                # sys.stdout.write(search[tweetIndex].text.encode('utf-8')+'\n')
                # sys.stdout.write(options.separator)
            count += number_to_get
            time.sleep(options.pausetime)
