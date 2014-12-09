from tweet import *
import symbolic_features

def getRashmiFeatures(tweet_content):
    f_list = []
    
    f_list += symbolic_features.smiley_count(tweet_content)

#     f_list.append(Feature("num_words2", len(tweet_content)))
#     f_list += f_list1
    return f_list
