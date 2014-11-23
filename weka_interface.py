

__author__ = 'yogarshi'

import os
import sys

weka = '/Users/yogarshi/Documents/weka-3-6-11/'


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
    train_with_cv("data.arff", 4)
    train_with_test()


if __name__ == "__main__":
    main()



