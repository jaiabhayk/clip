from tweet import *

def getYogarshiFeatures(tweet_content):
    f_list = []

    f_list.append(Feature("num_words1", len(tweet_content)))
#     #feature_list += sample_feature(tweet_content)
#     feature_list += sample_feature2(tweet_content)
#     #feature_list += num_words(tweet_content)
#     feature_list += add_bigrams(tweet_content)
#     feature_list += add_trigrams(tweet_content)
    
#     f_list += f_list1
    return f_list