from tweet import *
import symbolic_features
import punctuations
import dependency_features

def getRashmiFeatures(tweet):
    f_list = []
    
    f_list += symbolic_features.smiley_count(tweet.tokenized)
    f_list += punctuations.punctuation_count(tweet.tokenized)
    #f_list += dependency_features.root_count(tweet.dep_parse)
    #f_list += dependency_features.dependency_path(tweet.dep_parse)
    f_list += dependency_features.dependency_pathdfs(tweet.dep_parse)
#     f_list.append(Feature("num_words2", len(tweet_content)))
#     f_list += f_list1
    return f_list
