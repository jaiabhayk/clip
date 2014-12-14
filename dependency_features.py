__author__ = 'rashmi'

from tweet import *
from senti_wordnet_features import *
from nltk.stem.porter import *
from nltk.stem.wordnet import WordNetLemmatizer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

senti_word_dict = populate_senti_word_dict('senti_wordnet_dictionary.txt')

def root_count(tweet_depparse):
    f_list=[]
    for each_token in tweet_depparse:
        if each_token[6] == '0' and each_token[1].isalnum():
            pos = each_token[3]
            token = lemmatizer.lemmatize(each_token[1].lower().decode('utf-8')).encode('utf-8')
            key = ''.join([token, "#", pos])
            if key not in senti_word_dict: 
                #print key
                continue
                
            score = senti_word_dict[key]
            #senti=senti_word_dict[each_token[1]+"#"+each_token[3]]
            print score
            f_list.append(Feature(each_token[1]+"_head",score))
    
    return f_list
