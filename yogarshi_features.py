from tweet import *
import mixed_bag


def getYogarshiFeatures(tweet_content):
    f_list = []

    f_list += mixed_bag.combine_features(tweet_content)

    return f_list