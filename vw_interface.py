__author__ = 'yogarshi'

import os
import sys
import numpy
import re

path_to_vw = '/usr/local/bin/vw'


def get_loss(output):
    """
    Pull out average loss for each fold in kfold and report statistics
    :param output: The content of the file that contains test statistics of the kfolds
    :return:
    """


    loss = []
    pattern = 'average loss = (.*?)\n'

    for each in re.finditer(pattern, output):

        #curr_loss = float(each.group( 1 ))
        loss.append(float(each.group(1)))


    mean = numpy.mean(loss)
    stdev = numpy.std(loss)
    print "Fold-wise loss = " + str(loss)
    print "Mean loss = " + str(mean)
    print "Std-dev = " + str(stdev)


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
            f.write('| ')
            f.write('i ')
            f.write(each_tweet.featureList[-1].name)
            f.write(':')
            f.write(str(each_tweet.featureList[-1].value))
            f.write(' ')
            f.write('\n')

def train_vw(training_file, quiet=False):
    """
    Train vw
    :param training_file:
    :return:
    """
    command = "rm *.cache"
    os.system(command)
    command = "rm model.vw"
    os.system(command)
    command = path_to_vw + ' -d ' + training_file + ' --holdout_off -b 25 -f model.vw --ignore i '
    if quiet:
        command += "--quiet"

    os.system(command)


def test_vw(test_file, quiet=False):
    """
    Test vw
    :param test_file:
    :return:
    """
    command = path_to_vw + ' -d ' + test_file + ' -t -i model.vw -p predictions.vw --ignore i '
    if quiet:
        command += "--quiet"
    os.system(command)


def test_vw_kfold(test_file, quiet=False):
    """
    Test vw
    :param test_file:
    :return:
    """
    command = path_to_vw + ' -d ' + test_file + ' -t -i model.vw -p predictions.vw --ignore i 2>>kFoldOutput'
    if quiet:
        command += "--quiet"
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

    count = 0
    pred_file = open("predictions.vw", 'r')
    out_file = open("Predic2tions.txt", 'w')
    for each_tweet in test_tweet_list:
        pred = float(pred_file.readline().strip())
        val = float(each_tweet.score)
        if abs(pred-val) > threshold:
            count += 1
            #out_file.write(str(each_tweet.id))
            #out_file.write('\n')
            #out_file.write(each_tweet.content)
            #out_file.write('\n')
            #out_file.write(str(each_tweet.tokenized))
            #out_file.write('\n')
            out_file.write(str(val))
            out_file.write('\t')
            out_file.write(str(pred))
            out_file.write('\n')
            #out_file.write('\n########################################################################\n')
        l1.append(val)
        l2.append(pred)

    correl = numpy.corrcoef(l1, l2)
    print correl
    print count

    pred_file.close()
    out_file.close()


def k_fold(train_tweet_list, k=10):


    main_list = []
    for i in range(k):
        main_list.append([])

    for i in range(len(train_tweet_list)):
        main_list[i%10].append(train_tweet_list[i])

    #Make sure folder exists
    if "kfoldstuff" not in  os.listdir('.'):
        os.system("mkdir kfoldstuff")
    #Delete results of previous kfold run
    if "kFoldOutput" in os.listdir('.'):
        os.system("rm kFoldOutput")

    #Prepare the files
    for i in range(k):
        train_file = "./kfoldstuff/Training" + str(i) + ".vw"
        test_file = "./kfoldstuff/Test" + str(i) + ".vw"

        test_tweets = main_list[i]
        train_tweets = []
        for j in range(k):
            if j != i:
                train_tweets += main_list[j]

        write_to_file(train_tweets, train_file)
        write_to_file(test_tweets, test_file)

        train_vw(train_file, quiet=True)


        test_vw_kfold(test_file)


    f = open("kFoldOutput", 'r')
    lines = f.read()
    get_loss(lines)
    #print "Average Loss for K-fold crossvalidation = " + str(loss)


if __name__ == "__main__":

    f = open("kFoldOutput", 'r')
    lines = f.read()

    loss = get_loss(lines)
    print "Average Loss for K-fold crossvalidation = " + str(loss)
    pass







