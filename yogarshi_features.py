from tweet import *
import mixed_bag


def getYogarshiFeatures(tweet):
    f_list = []

    f_list += mixed_bag.combine_features(tweet.tokenized)

    return f_list