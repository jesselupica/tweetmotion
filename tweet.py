from collections import MutableSequence
from collections import namedtuple

class Tweet(MutableSequence):
    def __init__(self, words, tags, trainer=True):
        assert len(words) == len(tags)
        TweetWord = namedtuple('TweetWord', ['word', 'tag'])
        if trainer:
            self.tokens = [TweetWord("<START>", "TWEET_START")]
        else:
            self.tokens = []
        for w, t in zip(words, tags):
            self.tokens.append(TweetWord(w, t))

    def add_sentence_tags(self, emotion, sentiment):
        self.emotion = emotion
        self.sentiment = sentiment

    def get_emotion(self):
        try:
            return self.emotion
        except NameError:
            raise AttributeError("Error: sentence level tagging not done")

    def get_sentiment(self):
        try:
            return self.sentiment
        except NameError:
            raise AttributeError("Errror: sentence level tagging not done")

    def insert(self, index, item):
        self.tokens.insert(index, item)

    def __setitem__(self, index, item):
        self.tokens[index] = item

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, index):
        return self.tokens[index]

    def __delitem__(self, index):
        del self.tokens[index]

    def __str__(self):
        return str(self.tokens)