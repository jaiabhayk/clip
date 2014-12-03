from tweet import *

__author__ = 'yogarshi'

import os
import sys
import collections

#weka = '/Users/yogarshi/Documents/weka-3-6-11/'

def write_to_file(filename, feature_name_dict, modified_tweet_list, total_feats):
    """
    Function to write the data to arff format

    :param filename:
    :param feature_name_dict:
    :param modified_tweet_list:
    :param total_feats:
    :return:
    """
    f = open(filename, 'w')
    f.write("@relation tweet_sentiments\n\n")

    feature_name_list = sorted([(feature_name_dict[key], key) for key in feature_name_dict])
    for each_feature_name in feature_name_list:
        f.write("@attribute\t")
        f.write(each_feature_name[1])
        f.write("\t")
        f.write("numeric\n")
    #f.write("@attribute\ttweet_id\tnumeric\n")
    f.write("@attribute\ttweet_score\tnumeric\n\n")


    #Now write stuff about all tweets back to file as well in sparse ARFF format
    f.write("@DATA\n")
    print len(modified_tweet_list)
    for each_tweet in modified_tweet_list:
        f.write('{')
        for each_feature in each_tweet[:-2]:
            index = each_feature[0]
            value = each_feature[1]

            f.write(str(index))
            f.write(' ')
            f.write(str(value))
            f.write(', ')

        #f.write(str(total_feats))
        #f.write(' ')
        #f.write(str(each_tweet[-2]))
        #f.write(', ')

        f.write(str(total_feats))
        f.write(' ')
        f.write(str(each_tweet[-1]))
        f.write("}\n")

    f.close()


def create_arff_file(training_tweet_list, training_file, test_tweet_list, test_file):
    """
    Reformats data so that it can easily be written to arff files.

    :param tweetList: List of Tweet objects
    :param filename: The file name to which to write
    :return:
    """

    #get the total number of unique features
    feature_name_dict = {}
    total_feats = 0

    #This will be used to write data back to file
    modified_train_tweet_list = []

    for each_tweet in training_tweet_list:

        modified_feature_list = []

        features_list = each_tweet.featureList
        for each_feature in features_list:
            if each_feature.name not in feature_name_dict:
                feature_name_dict[each_feature.name] = total_feats
                total_feats += 1
                modified_feature_list.append((total_feats-1, each_feature.value))
            else:
                modified_feature_list.append((feature_name_dict[each_feature.name], each_feature.value))


        #Append the score at the end as well
        modified_train_tweet_list.append(sorted(modified_feature_list))
        modified_train_tweet_list[-1].append(each_tweet.id)
        modified_train_tweet_list[-1].append(each_tweet.score)


    #If we have been supplied a test_file, then we need to get the features from the test set as well
    if test_file is not None:
        modified_test_tweet_list = []

        for each_tweet in test_tweet_list:
            modified_feature_list = []

            features_list = each_tweet.featureList
            for each_feature in features_list:
                if each_feature.name not in feature_name_dict:
                    feature_name_dict[each_feature.name] = total_feats
                    total_feats += 1
                    modified_feature_list.append((total_feats-1, each_feature.value))
                else:
                    modified_feature_list.append((feature_name_dict[each_feature.name], each_feature.value))


            #Append the score at the end as well
            modified_test_tweet_list.append(sorted(modified_feature_list))
            modified_test_tweet_list[-1].append(each_tweet.id)
            modified_test_tweet_list[-1].append(each_tweet.score)


    #write info about all features to training_file
    write_to_file(training_file, feature_name_dict, modified_train_tweet_list, total_feats)
    write_to_file(test_file, feature_name_dict, modified_test_tweet_list, total_feats)



def train_with_cv(trainFile, folds):
    """
    Train a Linear Regression function and evaluate by cross-validation. The train file has to be in arff format.
    :param trainFile: The training data file
    :param folds: The number of folds for cross_validation
    :return:
    """

    command = 'java weka.classifiers.functions.LinearRegression -t ' + trainFile + ' -x ' + str(folds) #+ ' -p 0'
    os.system(command)


def train_with_test(trainFile, testFile):
    """
    Train a Linear Regression function and evaluate on a test set. The train and test files have to be in arff format.
    :param trainFile: The training data file
    :param testFile: The test data file
    :return:
    """

    command = 'java -Xmx8192m weka.classifiers.functions.LinearRegression -t ' + trainFile + ' -T ' + testFile #+' -p 0'
    os.system(command)


