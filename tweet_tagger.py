import os
import sys
import termcolor 

input_file = sys.argv[1]
#output_file = sys.argv[2]
#def get_tweets_from_file(input_file, output):
f = open(input_file, 'r')
tweets = f.readlines()

emotion_tags = ["Happy", "Angry", "Thoughtful", "Excited", "Funny", "Neutral", "Sad"]

for tweet in tweets:
    words = tweet.split()
    seen_words = []
    for word in words:
        colored_word = termcolor.colored(word, 'red', 'on_white')
        sys.stdout.write("\r%s " % (' '.join(seen_words + [colored_word]).rstrip()))
        sys.stdout.flush()
        seen_words.append(word)
        raw_input("\r\b")
