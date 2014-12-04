__author__ = 'yogarshi'
import os
import sys

path_to_vw = '/usr/local/bin/vw'


def write_to_file(tweet_list, out_file):

    with open(out_file, 'w') as f:

        for each_tweet in tweet_list:
            f.write(str(each_tweet.score))
            f.write(' | ')
            for each_feature in each_tweet.featureList:
                f.write(str(each_feature.name))
                f.write(':')
                f.write(str(each_feature.value))
                f.write(' ')

            f.write('\n')

def train_vw(training_file):
    command = path_to_vw + ' -d' + training_file + ' -c --passes=10 -b 25 -f model.vw'
    os.system(command)

def test_vw(test_file):
    command = path_to_vw + ' -d ' + test_file + ' -i model.vw -p predictions.txt'
    os.system(command)
