from tweet import Tweet

def process_file(name):
    with open(name, 'r') as f:
        words = []
        tags = []
        tweets = []
        for line in f:
            line = line.strip()
            if line != "---":
                line = line.split("|")
                assert len(line) == 2
                words.append(line[0])
                tags.append(line[1])
            else:
                tweets.append(Tweet(words, tags))
                words = []
                tags = []

    return tweets