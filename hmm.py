from __future__ import division
from collections import Counter
from collections import namedtuple
from tweet import Tweet
from processor import process_file
from tqdm import tqdm
import argparse
import clusters 

TAGS = ['TWEET_START', 'HAPPY', 'SAD', 'NEUTRAL', 'ANGRY', 'EXCITED', 'FUNNY', 'THOUGHTFUL']

class HiddenMarkovModel(object):
    def __init__(self, train_data):
        self.tag_pair_counts = Counter()
        self.tag_counts = Counter()
        self.word_tag_counts = Counter()

        for tweet in tqdm(train_data):
            self.tag_counts.update(x.tag for x in tweet)
            self.tag_pair_counts.update((x.tag, y.tag) for x,y in zip(tweet, tweet[1:]))
            self.word_tag_counts.update((clusters.get_cluster_id(x.word), x.tag) for x in tweet)


    def _get_tag_probability(self, t1, t2):
        return self.tag_pair_counts[t1, t2] / self.tag_counts[t1]

    def _get_word_tag_probability(self, word, tag):
        return self.word_tag_counts[clusters.get_cluster_id(word), tag] / self.tag_counts[tag]

    def tag_tweet(self, tweet):
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
            i -= 1

        seq = reversed(seq)
        return Tweet(tweet, [x.tag for x in seq], trainer=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tweet mood tagger CS 4701")
    parser.add_argument("training_tweets")

    args = parser.parse_args()
    tweets = process_file(args.training_tweets)
    h = HiddenMarkovModel(tweets)
    while True:
        x = raw_input()
        x = x.split()
        print h.tag_tweet(x)