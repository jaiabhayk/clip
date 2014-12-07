from tweet import *
from hash_tag_features import *

def getAbhayFeatures(tweet_content):
    f_list = []
    f_list += getHashTagFeatures(tweet_content)
    return f_list