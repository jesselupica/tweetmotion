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

tag_random_cluster:
	python hmm.py data/all_training_tweets.txt

tag_random_no_cluster:
	python hmm.py data/all_training_tweets.txt --no_cluster

human_compare:
	python test_agreement.py data/jesse_test_tweets.txt data/jimmy_test_tweets.txt

file_demo_no_cluster:
	python hmm.py data/all_training_tweets.txt --untagged_data data/demo_tweets.txt --no_cluster

file_demo_cluster:
	python hmm.py data/all_training_tweets.txt --untagged_data data/demo_tweets.txt

manual_demo_cluster:
	python hmm.py data/all_training_tweets.txt --manual_entry

manual_demo_no_cluster:
	python hmm.py data/all_training_tweets.txt --manual_entry --no_cluster


deps:
	echo "You must have Python (2) and pip installed to run this program"
	pip install -r requirements.txt
	echo "Done installing dependencies"
	