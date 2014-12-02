__author__ = 'yogarshi'
"""
This is the code that has to be run.
"""

from weka_interface import *
import sys
from twokenize import *

def sample_feature(tweet_content):

    f_list = []
    for each_word in tweet_content:
        f_list.append(Feature(each_word, 1))

    return f_list



def read_tweets(filename):
    """
    Read the tweet data from a file and store in tweet objects. Tokenize using Twitter tokenizer
    :param filename:
    :return:
    """
     ## TODO: Abhay

    tweet_list = list()

    tweet_list.append(Tweet(1, tokenize("This is a test tweet #Works"), 0))
    tweet_list.append(Tweet(2, tokenize("This is another test tweet :( #Works"), -1))
    tweet_list.append(Tweet(3, tokenize("This is the last test tweet :) #Works"), 1))
    return tweet_list


def get_features(tweet_content):
    ### TODO: Using a toy feature right now to check all other parts of the code. This function will call all other
    ### TODO: feature extraction functions

    feature_list = []

    feature_list += sample_feature(tweet_content)

    return feature_list


def main(argv):

    if len(argv) > 2:
        print "Incorrect number of arguments. Usage python analyze_sentiment.py <training_data_file> [<test_data_file>]"
        sys.exit()

    ###TODO: Use argparse to handle command line arguments

    train_file_raw = argv[0]
    test_file_raw = None
    folds = 2                 ### TODO: Make this a command line parameter

    training_file_arff = "TrainingSet.arff"
    test_file_arff = "TestSet.arff"


    # Check if testfile has been provided
    if len(argv) == 2:
        test_file_raw = argv[1]



    #Read the tweets and store in a tokenized form
    training_tweet_list = read_tweets(train_file_raw)
    if test_file_raw is not None:
        test_tweet_list = read_tweets(test_file_raw)



    #Assemble the features
    for each_tweet in training_tweet_list:
        each_tweet.featureList = get_features(each_tweet.content)

    if test_file_raw is not None:
        for each_tweet in test_tweet_list:
            each_tweet.featureList = get_features(each_tweet.content)



    #Create training and testing files
    create_arff_file(training_tweet_list, training_file_arff)
    if test_file_raw is not None:
        create_arff_file(test_tweet_list, test_file_arff)



    #If test file is given, perform training with evaluation on the test set, else do k fold cross-validation
    if test_file_raw is not None:
        train_with_test(training_file_arff, test_file_arff)
    else:
        train_with_cv(training_file_arff, folds)



if __name__ == "__main__":
    main(sys.argv[1:])
