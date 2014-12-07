__author__ = 'yogarshi'
"""
Mixed bag of features
"""

from tweet import *

def num_capital(tweet_content):

    val = 0
    for each_token in tweet_content:
        if each_token.isupper():
            val += 1

    return [Feature("num_capital", val)]


def add_bigrams(tweet_content):

    f_list = []
    bi_dict = {}
    for i in range(len(tweet_content)-1):
        if tweet_content[i].isalnum() and tweet_content[i+1].isalnum():
            t = tweet_content[i].lower() + '_' + tweet_content[i+1].lower()
            if t not in bi_dict:
                bi_dict[t] = 0
            bi_dict[t] +=1

    for each in bi_dict:
        f_list.append(Feature(each, bi_dict[each]))
    return f_list


def add_trigrams(tweet_content):

    f_list = []
    tri_dict = {}
    for i in range(len(tweet_content)-2):
        if tweet_content[i].isalnum() and tweet_content[i+1].isalnum() and tweet_content[i+2].isalnum():
            t = tweet_content[i].lower() + '_' + tweet_content[i+1].lower() + '_' + tweet_content[i+2].lower()
            if t not in tri_dict:
                tri_dict[t] = 0
            tri_dict[t] += 1

    for each in tri_dict:
        f_list.append(Feature(each, tri_dict[each]))
    return f_list

def is_retweet(tweet_content):

    if tweet_content[0] == "RT":
        return [Feature("is_retweet", 1)]
    else:
        return [Feature("is_retweet", 0)]


def num_at_mentions(tweet_content):
    val = 0
    for each_token in tweet_content:
        if each_token[0] == '@':
            val += 1

    return [Feature("num_at_mentions", val)]


def combine_features(tweet_content):

    f_list = []

    f_list += num_capital(tweet_content)
    f_list += add_bigrams(tweet_content)
    f_list += add_trigrams(tweet_content)
    f_list += is_retweet(tweet_content)
    f_list += num_at_mentions(tweet_content)


    return f_list





