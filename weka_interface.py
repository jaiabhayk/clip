from tweet import *

__author__ = 'yogarshi'

import os
import sys
import collections

#weka = '/Users/yogarshi/Documents/weka-3-6-11/'


def create_arff_file(tweetList, filename):
    """
    Create an arff file given a list of tweet objects. Right now, assuming that all tweets have the same features.

    :param tweetList: List of Tweet objects
    :param filename: The file name to which to write
    :return:
    """

    with open(filename+".arff", 'w') as f:

        f.write("@relation tweet_sentiments\n\n")

        #get the total number of unique features
        feature_name_dict = {}
        total_feats = 0

        #This will be used to write data back to file
        modified_tweet_list = []

        for each_tweet in tweetList:

            modified_feature_list = []

            features_list = each_tweet.featureList
            for each_feature in features_list:
                if each_feature.name not in feature_name_dict:
                    feature_name_dict[each_feature.name] = total_feats
                    total_feats += 1
                    modified_feature_list.append((total_feats-1, each_feature.value))
                else:
                    modified_feature_list.append((feature_name_dict[each_feature.name], each_feature.value))

            modified_tweet_list.append(sorted(modified_feature_list))
            #Append the score at the end as well
            modified_tweet_list.append(each_tweet.score)

        #write info about all features to file
        feature_name_list = sorted([(feature_name_dict[key], key) for key in feature_name_dict])
        for each_feature_name in feature_name_list:
            f.write("@attribute\t")
            f.write(each_feature_name)
            f.write("\t")
            f.write("numeric\n")
        f.write("score\tnumeric\n\n")


        #Now write stuff about all tweets back to file as well in sparse ARFF format
        f.write("@DATA\n\n")
        for each_tweet in modified_tweet_list:
            f.write('{')
            for each_feature in each_tweet[:-1]:
                index = each_feature[0]
                value = each_feature[1]

                f.write(str(index))
                f.write(' ')
                f.write(str(value))
                f.write(', ')

            f.write(str(total_feats))
            f.write(' ')
            f.write(str(each_tweet[-1]))
            f.write("}\n")



def train_with_cv(trainFile, folds):
    """
    Train a Linear Regression function and evaluate by cross-validation. The train file has to be in arff format.
    :param trainFile: The training data file
    :param folds: The number of folds for cross_validation
    :return:
    """

    command = 'java weka.classifiers.functions.LinearRegression -t ' + trainFile + ' -x ' +str(folds)
    os.system(command)


def train_with_test(trainFile, testFile):
    """
    Train a Linear Regression function and evaluate on a test set. The train and test files have to be in arff format.
    :param trainFile: The training data file
    :param testFile: The test data file
    :return:
    """

    command = 'java weka.classifiers.functions.LinearRegression -t ' + trainFile + ' -T ' + testFile
    os.system(command)


def main():
    pass

if __name__ == "__main__":
    main()



