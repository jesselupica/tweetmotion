from __future__ import division

import twitter

ENGLISH_WORD_PERCENTAGE = .5

f=open("account","r") #this file should contain "consumer_key consumer_secret access_token_key access_token_secret"
acc=f.read().split()
f.close()

api=twitter.api.Api(consumer_key=acc[0], consumer_secret=acc[1], access_token_key=acc[2], access_token_secret=acc[3])


lis = api.GetStreamSample()

with open('/usr/share/dict/words','r') as w:
    words = set(c.strip() for c in w.readlines())


def get_tweet():
    for tweet in lis:
        try:
            l = len(tweet['text'].split())
            count = 0
            for word in tweet['text'].split():
                if word in words:
                    count += 1
            if count/l > ENGLISH_WORD_PERCENTAGE:
                try:
                    return tweet['text'].replace("\n", " ")
                except:
                    pass
            else:
                pass
                #print "not english"
                #print tweet['text']
        except KeyError:
            pass
            #print "deleted tweet"

if __name__ == '__main__':
    while True:
        print get_tweet().encode('utf-8')