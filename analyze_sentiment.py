"""
This is the code that has to be run.
"""

#from weka_interface import *
import sys
import time
from twokenize import *
from vw_interface import *
from tweet import *
import mixed_bag
from mixed_bag import *


def read_tweets(filename):
    """
    Read the tweet data from a file and store in tweet objects. Tokenize using Twitter tokenizer
    :param filename:
    :return:
    """
    tweet_list = list()
    f = open(filename, 'r')
    for line in f.readlines():
        values = line.split("\t");
        if len(values) > 3:
            print 'Unexpected tweet'
            sys.exit()
            
        id = values[0]
        text = values[2]
        score = values[1]
        tweet_list.append(Tweet(id, text, tokenize(text), score))
    f.close()
    return tweet_list


def get_features(tweet_content):
    # ## TODO: Using a toy feature right now to check all other parts of the code. This function will call all other
    # ## TODO: feature extraction functions

    feature_list = []

    return feature_list


def main(argv):

    if len(argv) > 2:
        print "Incorrect number of arguments. Usage python analyze_sentiment.py <training_data_file> [<test_data_file>]"
        sys.exit()

    # ##TODO: Use argparse to handle command line arguments

    train_file_raw = argv[0]
    test_file_raw = None
    folds = 5  # ## TODO: Make this a command line parameter

    training_file = "TrainingSet.vw"
    test_file = "TestSet.vw"


    # Check if testfile has been provided
    if len(argv) == 2:
        test_file_raw = argv[1]



    # Read the tweets and store in a tokenized form
    training_tweet_list = read_tweets(train_file_raw)
    test_tweet_list = []
    if test_file_raw is not None:
        test_tweet_list = read_tweets(test_file_raw)


    # Assemble the features
    for each_tweet in training_tweet_list:
        each_tweet.featureList = get_features(each_tweet.tokenized)
        each_tweet.featureList.append(Feature("tweet_id", each_tweet.id))

    if test_file_raw is not None:
        for each_tweet in test_tweet_list:
            each_tweet.featureList = get_features(each_tweet.tokenized)
            each_tweet.featureList.append(Feature("tweet_id", each_tweet.id))


    # Create training and testing files
    #create_arff_file(training_tweet_list, training_file, test_tweet_list, test_file)
    write_to_file(training_tweet_list, training_file)
    write_to_file(test_tweet_list, test_file)


    #Do vw stuff
    #start_time = time.time()
    train_vw(training_file)
    test_vw(test_file)
    print len(test_tweet_list)
    map_predictions(test_tweet_list, 0)


if __name__ == "__main__":
    main(sys.argv[1:])
