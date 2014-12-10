from tweet import *
from hash_tag_features import *
from senti_wordnet_features import *

def getAbhayFeatures(tweet):
    f_list = []
    f_list += getHashTagFeatures(tweet.tokenized)
    f_list += getSentiScoreFeatures(tweet)
    return f_list