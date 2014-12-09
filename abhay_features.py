from tweet import *
from hash_tag_features import *
from senti_wordnet_features import *

def getAbhayFeatures(tweet_content):
    f_list = []
    f_list += getHashTagFeatures(tweet_content)
    f_list += getSentiScoreFeatures(tweet_content)
    return f_list