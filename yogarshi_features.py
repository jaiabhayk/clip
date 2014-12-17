from tweet import *
import mixed_bag
import POSFeatures
import lexicon_features
import depParseFeatures


def getYogarshiFeatures(tweet):
    f_list = []

    f_list += mixed_bag.combine_features(tweet.tokenized)
    f_list += POSFeatures.combine_features(tweet)
    f_list += lexicon_features.combine_features(tweet)
    f_list += depParseFeatures.combine_features(tweet)
    return f_list