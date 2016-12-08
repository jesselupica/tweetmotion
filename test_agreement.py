from __future__ import division
from processor import process_file
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_one")
parser.add_argument("file_two")
args = parser.parse_args()


tweets_one = process_file(args.file_one)
tweets_two = process_file(args.file_two)


assert(len(tweets_one) == len(tweets_two))  
percent_matches = []
sentence_sent_tag_matches = []
sentence_emo_tag_matches = []
for t_tweet, mt_tweet in zip(tweets_one, tweets_two):
    assert(len(t_tweet) == len(mt_tweet))
    matches = [t_w.tag == mt_w.tag for t_w, mt_w in zip(t_tweet, mt_tweet)]
    percent_matches.append(matches.count(True)/len(matches))
    sentence_emo_tag_matches.append(t_tweet.get_emotion() == mt_tweet.get_emotion())
    sentence_sent_tag_matches.append(t_tweet.get_sentiment() == mt_tweet.get_sentiment())

print "TEST DATA RESULTS:"
print "--------------------------------"
print "average token match rate: " + str(round(sum(percent_matches)/len(percent_matches) * 100, 2)) + '%'
print "average sentence level match rate: " + str(round(sentence_sent_tag_matches.count(True)/len(sentence_sent_tag_matches) * 100, 2))  + '%'
print "average emotion match rate: " + str(round(sentence_emo_tag_matches.count(True)/len(sentence_emo_tag_matches)*100, 2)) + '%'
