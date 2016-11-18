import sys
import termcolor 
from getch import getch

input_file = sys.argv[1]
output_file = sys.argv[2]
f = open(input_file, 'r')
tweets = f.readlines()

TAG_MAP = {
    'h' : "HAPPY",
    'a' : "ANGRY",
    't' : "THOUGHTFUL",
    'e' : "EXCITED",
    'f' : "FUNNY",
    'n' : "NEUTRAL",
    's' : "SAD"
}

emotion_tags = ["Happy", "Angry", "Thoughtful", "Excited", "Funny", "Neutral", "Sad"]

def save_tweets(tag_seq):
    of = open(output_file, 'a')

    for tag_pair in tag_seq:
        of.write(tag_pair[0] + "|" + tag_pair[1] + '\n')
    of.write("---\n")
    of.close()

with open(output_file, 'r') as f:
    start = sum(1 for l in f if l.strip() == "---")

tweet_tags = []
for tweet in tweets[start:]:
    words = tweet.split()
    if words[0] == "RT" or words[1][0] == "@":
        start = 2
    else:
        start = 0
    tags = []
    for i, word in enumerate(words[start:], start):
        for x in TAG_MAP.items():
            print x
        while True:
            try:
                to_write = words[:]
                to_write[i] = termcolor.colored(word, 'red')
                print ' '.join(to_write).rstrip()
                print ""
                tag = TAG_MAP[getch()]
            except:
                print "Invalid tag"
                continue
            tags.append((word, tag))
            break
    save_tweets(tags)
    print termcolor.colored(emotion_tags, 'green')

f.close()