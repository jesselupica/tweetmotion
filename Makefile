jesse_cluster:
	python hmm.py data/all_training_tweets.txt --test_model --untagged_data data/untagged_test_tweets.txt --tagged_data data/jesse_test_tweets.txt

jimmy_cluster:
	python hmm.py data/all_training_tweets.txt --test_model --untagged_data data/untagged_test_tweets.txt --tagged_data data/jimmy_test_tweets.txt

all_cluster:
	python hmm.py data/all_training_tweets.txt --test_model --untagged_data data/untagged_test_tweets.txt \
	--tagged_data data/jesse_test_tweets.txt --tagged_data data/jimmy_test_tweets.txt

jesse_no_cluster:
	python hmm.py data/all_training_tweets.txt --test_model --untagged_data data/untagged_test_tweets.txt --tagged_data data/jesse_test_tweets.txt --no_cluster

jimmy_no_cluster:
	python hmm.py data/all_training_tweets.txt --test_model --untagged_data data/untagged_test_tweets.txt --tagged_data data/jimmy_test_tweets.txt --no_cluster

all_no_cluster:
	python hmm.py data/all_training_tweets.txt --test_model --untagged_data data/untagged_test_tweets.txt \
	--tagged_data data/jesse_test_tweets.txt --tagged_data data/jimmy_test_tweets.txt --no_cluster

tweets:
	python -u tweetbot.py

tag_random:
	python hmm.py data/all_training_tweets.txt

human_compare:
	python test_agreement.py data/jesse_test_tweets.txt data/jimmy_test_tweets.txt