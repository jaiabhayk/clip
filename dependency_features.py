__author__ = 'rashmi'

from tweet import *
from senti_wordnet_features import *
from nltk.stem.porter import *
from nltk.stem.wordnet import WordNetLemmatizer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

senti_word_dict = populate_senti_word_dict('senti_wordnet_dictionary.txt')
tags=['n','v','a','r']
def root_count(tweet_depparse):
    f_list=[]
    #print lemmatizer.lemmatize("complaining".decode('utf-8')).encode('utf-8')
    for each_token in tweet_depparse:
        if each_token[6] == '0' and each_token[1].isalnum():
            pos = each_token[3].lower()
            token = lemmatizer.lemmatize(each_token[1].lower().decode('utf-8')).encode('utf-8')
            key = ''.join([token, "#", pos])
            """
            if key not in senti_word_dict:
                for p in tags:
                    tempkey=''.join([token,"#",p])
                    if tempkey in senti_word_dict:
                        key=tempkey
                        break
            """
            if key not in senti_word_dict:
                #print key
                continue
                
            score = senti_word_dict[key]
            #senti=senti_word_dict[each_token[1]+"#"+each_token[3]]
            #print score
            if score>0:
                f_list.append(Feature(each_token[1].join("_head"),1))
            else:
                f_list.append(Feature(each_token[1].join("_head"),-1))
    return f_list
