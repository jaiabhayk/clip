import sys
import time
from twokenize import *
from vw_interface import *
from tweet import *
from collections import Counter

def getHashTagFeatures(tweet_content):
    f_list = []
    hashTags = Counter()
    for token in tweet_content:
            if token[0] == '#':
                token = normalizeHashTag(token)
                if token is None:
                    unused = 1;
#                     print '\n Ignoring hashTag:- ', token, '=', hashTags[token]
                else:
                    hashTags[token] += 1
#                     print '\n hashTag:- ', token, '=', hashTags[token]
                    
#     print '\n All hash tags frequencies:- \n', hashTags
    for tag in hashTags:
        f_list.append(Feature(tag, hashTags[tag]))
        
#     print '\n Hash Tag Features List:-\n'
#     for f in f_list:
#         print f, '\t'

    return f_list

def normalizeHashTag(tag):
    """
    Use this method to normalize the hash tag. Normalization include changing to lower case and 
    also using eqquivalance class name for any tag. 
    Return None if the tag should not be considered
    """
    supported_hash_tags = ['#sarcasm', '#not', '#irony', "#yeahright"]
    if tag.lower() not in supported_hash_tags:
        return None
    else:
        return tag.lower();
    

def getHashTagFrequencies(tweet_list):
    hashTags = Counter()
    for tweet in tweet_list:
        print tweet.content, '\n'
        for token in tweet.content:
            token = token.lower()
            if token[0] == '#':
                hashTags[token] += 1
                print '\n hashTag:- ', token, '=', hashTags[token]
                
    print '\n All hash tags frequencies:- \n', hashTags
                
            
    return []


    

    
