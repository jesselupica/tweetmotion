import os
import sys
import termcolor 

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


tweet_tags = []
for tweet in tweets:
    words = tweet.split()
    tags = []
    for i, word in enumerate(words):
        while True:
            try:
                to_write = words[:]
                to_write[i] = termcolor.colored(word, 'red')
                sys.stdout.write("\r%s " % (' '.join(to_write).rstrip()))
                sys.stdout.flush()
                tag = TAG_MAP[raw_input()]
            except:
                print "Invalid tag"
                continue
            tags.append((word, tag))
            print(chr(27) + "[2J")
            break
    save_tweets(tags)
    print termcolor.colored(emotion_tags, 'green')

f.close()