__author__ = 'rashmi'

from tweet import *

def punctuation_count(tweet_content):
    f_list=[]
    counte=0
    countq=0
    maxcounte=0
    maxcountq=0
    prevcounte=0
    prevcountq=0
    
    for each_token in tweet_content:
        if each_token[0]=='!':
            counte+=1
        if each_token[0]=='?':
            countq+=1

    for each_token in tweet_content:
        prevcounte=0
        prevcountq=0
        if each_token[0]=='!':
            for char_token in each_token:
                if char_token=='!':
                    prevcounte+=1
                else: break
            if prevcounte>maxcounte: maxcounte = prevcounte    
        
        if each_token[0]=='?'or each_token[0]=='!':
            for char_token in each_token:
                if char_token=='!': 
                    prevcountq+=1
                elif char_token=='?':
                    prevcountq+=1
                else: break
            if prevcountq>maxcountq: maxcountq = prevcountq
    f_list.append(Feature("!count",maxcounte/len(tweet_content)))
    f_list.append(Feature("?count",maxcountq/len(tweet_content)))
    return f_list
