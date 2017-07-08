# tweetmotion
A twitter bot that guesses the emotion of a tweet. To learn more, read the CS_4701_Final.pdf paper, which is a detailed description of this project and its goals.

To run this program, view the Make targets. Run "make deps" to install all required Python dependencies.

After that, you should be able to successfully run all make target except tweets, tag_random_cluster, tag_random_no_cluster.
This is because these make targets pull down Tweets from Twitter live as they run, and thus require twitter credentials. If
you would like to run these targets, please acquire Twitter API credentials then put them in a file called "account" in
the root directory formatted like this:

consumer_key consumer_secret access_token_key access_token_secret

After that, tweetbot.py will be able to access your credentials and thus can pull down tweets to be tagged live from twitter.