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
POSITIVE_TAGS = set(['HAPPY', 'EXCITED', 'FUNNY'])
NEUTRAL_TAGS = set(['NEUTRAL', 'THOUGHTFUL'])
NEGATIVE_TAGS = set(['SAD', 'ANGRY'])

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
        return Tweet(tweet, tags, trainer=False)

    def sentence_tag_tweet(self, tagged_tweet):
        tags = Counter(w.tag for w in tagged_tweet)
        emotion = tags.most_common(1)[0][0]
        positive_score = sum(tags[tag] for tag in POSITIVE_TAGS)
        negative_score = sum(tags[tag] for tag in NEGATIVE_TAGS)
        neutral_score = sum(tags[tag] for tag in NEUTRAL_TAGS)
        sentiment = max([("POSITIVE", positive_score), ("NEGATIVE", negative_score), ("NEUTRAL", neutral_score)], key=lambda x : x[1])[0]
        tagged_tweet.add_sentence_tags(emotion, sentiment)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tweet mood tagger CS 4701")
    parser.add_argument("training_tweets", help="The tagged tweets to train the model")
    parser.add_argument("--no_clusters", help="Don't use word clusters", action="store_const", const=True, default=False)
    parser.add_argument("--test_model", help="Test model against tagged test set", default=None)

    args = parser.parse_args()
    tweets = process_file(args.training_tweets)
    model = HiddenMarkovModel(tweets, args.no_clusters)
    if not args.test_model:
        while True:
            raw_input()
            x = tweetbot.get_tweet()
            print x
            x = x.split()
            if x[0] == "RT" or x[1][0] == "@":
                x = x[2:]
            x = ['TWEET_START'] + x
            tagged_tweet = model.tag_tweet(x)
            model.sentence_tag_tweet(tagged_tweet)
            print "EMOTION: " + tagged_tweet.get_emotion()
            print "SENTIMENT: " + tagged_tweet.get_sentiment()
            print "--------------------------------"
            # Dont' print the start tag
            for w in tagged_tweet[1:]:
                print w.word + " : " + w.tag
    else:
        pass
