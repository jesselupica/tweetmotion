from __future__ import division
from collections import Counter
import string
from collections import namedtuple
from tweet import Tweet
from processor import process_file
from tqdm import tqdm
import argparse
import clusters 
import tweetbot

TAGS = ['TWEET_START', 'HAPPY', 'SAD', 'NEUTRAL', 'ANGRY', 'EXCITED', 'FUNNY', 'THOUGHTFUL']

class HiddenMarkovModel(object):
    def __init__(self, train_data, using_clusters=True):
        self.using_clusters=using_clusters
        self.tag_pair_counts = Counter()
        self.tag_counts = Counter()
        self.word_tag_counts = Counter()

        for tweet in tqdm(train_data):
            self.tag_counts.update(x.tag for x in tweet)
            self.tag_pair_counts.update((x.tag, y.tag) for x,y in zip(tweet, tweet[1:]))
            if self.using_clusters:
                self.word_tag_counts.update((clusters.get_cluster_id(x.word), x.tag) for x in tweet)
            else:
                self.word_tag_counts.update((x.word, x.tag) for x in tweet)
        self.epsilon = (min((x[1] for x in self.word_tag_counts.iteritems()))/max(x[1] for x in self.tag_counts.iteritems())) * .1


    def _get_tag_probability(self, t1, t2):
        return self.tag_pair_counts[t1, t2] / self.tag_counts[t1]

    def _get_word_tag_probability(self, word, tag):
        if self.using_clusters:
            if self.word_tag_counts[clusters.get_cluster_id(word), tag] > 0:
                return self.word_tag_counts[clusters.get_cluster_id(word), tag] / self.tag_counts[tag]
            else:
                return self.epsilon
        else:
            if self.word_tag_counts[word, tag] > 0:
                return self.word_tag_counts[word, tag] / self.tag_counts[tag]
            else:
                return self.epsilon

    def tag_tweet(self, tweet):
        tweet = tweet.split()
        if tweet[0] == "RT" or tweet[1][0] == "@":
            tweet = tweet[2:]
        tweet = ['TWEET_START'] + tweet
        for i, t in enumerate(tweet):
            new = "".join(c for c in t if c in string.ascii_letters + string.digits)
            if new != "":
                tweet[i] = new
        GraphNode = namedtuple('GraphNode', ['tag', 'prob', 'bptr'])
        graph = [[GraphNode(TAGS[0], 1.0, -1)]]
        for token in tweet[1:]: 
            graph.append([])
            for i, curr_tag in enumerate(TAGS[1:], 1):
                best_node = GraphNode(curr_tag, -1, -1)
                for i, prev_node in enumerate(graph[-2]):
                    node_prob = self._get_tag_probability(prev_node.tag, curr_tag) * self._get_word_tag_probability(token, curr_tag)
                    tag_prob = node_prob * prev_node.prob
                    if tag_prob > best_node.prob:
                        best_node = GraphNode(tag=curr_tag, prob=tag_prob, bptr=i)
                graph[-1].append(best_node)

        best_last_node = max(graph[-1], key=lambda x: x.prob)
        seq = [best_last_node]
        i = len(graph) - 2
        while(seq[-1].bptr != -1):
            seq.append(graph[i][best_last_node.bptr])
            best_last_node = graph[i][best_last_node.bptr]
            i -= 1

        seq = reversed(seq)
        tags =  [x.tag for x in seq]
        t = Tweet(tweet, tags, trainer=False)
        return t

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tweet mood tagger CS 4701")
    parser.add_argument("training_tweets", help="The tagged tweets to train the model")
    parser.add_argument("--no_clusters", help="Don't use word clusters", action="store_const", const=True, default=False)
    parser.add_argument("--test_model", help="Test model against tagged test set", action="store_const", const=True, default=False)
    parser.add_argument("--untagged_data", help="Untagged data for the model to run on", default=None)
    parser.add_argument("--tagged_data", help="Data to compare validity of model", default=[], action='append')

    args = parser.parse_args()
    tweets = process_file(args.training_tweets)
    model = HiddenMarkovModel(tweets, args.no_clusters)
    if not args.test_model:
        while True:
            raw_input()
            x = tweetbot.get_tweet()
            print x
            tagged_tweet = model.tag_tweet(x)
            print "EMOTION: " + tagged_tweet.get_emotion()
            print "SENTIMENT: " + tagged_tweet.get_sentiment()
            print "--------------------------------"
            # Dont' print the start tag
            for w in tagged_tweet[1:]:
                print w.word + " : " + w.tag
    else:
        tagged_tweets = list(zip(*tuple(map(process_file, args.tagged_data))))

        untagged_f = open(args.untagged_data, 'r')
        model_tagged_tweets = []
        untagged_tweets = untagged_f.readlines()
        for tweet in untagged_tweets: 
            model_tagged_tweets.append(model.tag_tweet(tweet))

        assert(len(tagged_tweets) == len(model_tagged_tweets))
        percent_matches = []
        sentence_sent_tag_matches = []
        sentence_emo_tag_matches = []
        for t_tweets, mt_tweet in zip(tagged_tweets, model_tagged_tweets):
            for t in t_tweets:
                assert(len(t) == len(mt_tweet))

            emotion_match = False
            sentiment_match = False
            matches = [False] * len(mt_tweet)
            for tweet in t_tweets:
                emotion_match = emotion_match or (tweet.get_emotion() == mt_tweet.get_emotion())
                sentiment_match = sentiment_match or (tweet.get_sentiment() == mt_tweet.get_sentiment())
                for i, (t_w, mt_w) in enumerate(zip(tweet, mt_tweet)):
                    matches[i] = matches[i] or (t_w.tag == mt_w.tag)

            percent_matches.append(matches.count(True)/len(matches))
            sentence_emo_tag_matches.append(emotion_match)
            sentence_sent_tag_matches.append(sentiment_match)

        print "TEST DATA RESULTS:"
        print "--------------------------------"
        print "average token match rate: " + str(round(sum(percent_matches)/len(percent_matches) * 100, 2)) + '%'
        print "average sentence level match rate: " + str(round(sentence_sent_tag_matches.count(True)/len(sentence_sent_tag_matches) * 100, 2))  + '%'
        print "average emotion match rate: " + str(round(sentence_emo_tag_matches.count(True)/len(sentence_emo_tag_matches)*100, 2)) + '%'
