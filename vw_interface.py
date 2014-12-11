__author__ = 'yogarshi'
import os
import sys
import numpy

path_to_vw = '/usr/local/bin/vw'


def write_to_file(tweet_list, out_file):
    """
    Create training and test file for use with vw
    :param tweet_list:
    :param out_file:
    :return:
    """

    with open(out_file, 'w') as f:

        for each_tweet in tweet_list:
            f.write(str(each_tweet.score))
            f.write(' | a ')
            for each_feature in each_tweet.featureList[:-1]:
                f.write(str(each_feature.name))
                f.write(':')
                f.write(str(each_feature.value))
                f.write(' ')
            f.write(' | ')
            f.write('i ')
            f.write(each_tweet.featureList[-1].name)
            f.write(':')
            f.write(str(each_tweet.featureList[-1].value))
            f.write(' ')
            f.write('\n')

def train_vw(training_file):
    """
    Train vw
    :param training_file:
    :return:
    """
    command = "rm *.cache"
    os.system(command)
    command = "rm model.vw"
    os.system(command)
    command = path_to_vw + ' -d ' + training_file + ' --holdout_off -b 25 -f model.vw --ignore i'

    os.system(command)

def test_vw(test_file):
    """
    Test vw
    :param test_file:
    :return:
    """
    command = path_to_vw + ' -d ' + test_file + ' -t -i model.vw -p predictions.vw --ignore i'
    os.system(command)


def map_predictions(test_tweet_list, threshold = 2):
    """
    Create human-readable predictions output file
    :param test_tweet_list:
    :param threshold:
    :return:
    """
    l1 = []
    l2 = []

    pred_file = open("predictions.vw", 'r')
    out_file = open("Predic2tions.txt", 'w')
    for each_tweet in test_tweet_list:
        pred = float(pred_file.readline().strip())
        val = float(each_tweet.score)
        if abs(pred-val) > threshold:
            out_file.write(str(each_tweet.id))
            out_file.write('\n')
            out_file.write(each_tweet.content)
            out_file.write('\n')
            out_file.write(str(each_tweet.tokenized))
            out_file.write('\n')
            out_file.write(str(val))
            out_file.write('\t')
            out_file.write(str(pred))
            out_file.write('\n')
            out_file.write('\n########################################################################\n')
        l1.append(val)
        l2.append(pred)

    correl = numpy.corrcoef(l1, l2)
    print correl

    pred_file.close()
    out_file.close()




