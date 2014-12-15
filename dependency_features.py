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
    poscount=0
    negcount=0
    #print lemmatizer.lemmatize("complaining".decode('utf-8')).encode('utf-8')
    for each_token in tweet_depparse:
        if each_token[6] == '0' and each_token[1].isalnum():
            pos = each_token[3].lower()
            token_word = each_token[1].lower()
            token_lemma = lemmatizer.lemmatize(each_token[1].lower().decode('utf-8')).encode('utf-8')
            token_stem = stemmer.stem(each_token[1].lower().decode('utf-8')).encode('utf-8')
            #check_list=[''.join([token_word,'#',pos]),''.join([token_lemma,'#',pos]),''.join([token_stem,'#',pos])]
            check_list=[''.join([token_word,'#',pos]),''.join([token_lemma,'#',pos]),''.join([token_stem,'#',pos]),''.join([token_word,'#','n']),''.join([token_word,'#','v']),''.join([token_word,'#','a']),''.join([token_word,'#','r']),''.join([token_lemma,'#','n']),''.join([token_lemma,'#','v']),''.join([token_lemma,'#','a']),''.join([token_lemma,'#','r']),''.join([token_stem,'#','n']),''.join([token_stem,'#','v']),''.join([token_stem,'#','a']),''.join([token_stem,'#','r'])]
            
            key=''.join([token_word,'#',pos])
            for i in check_list:
                if i in senti_word_dict:
                    key=i
                    break
                else: continue
            
            if key not in senti_word_dict:
                #print key
                continue
                
            score = senti_word_dict[key]
            #senti=senti_word_dict[each_token[1]+"#"+each_token[3]]
            #print score
            #f_list.append(Feature(each_token[1].lower().join("_head"),score))
            if score>0.1:
                poscount+=1
                f_list.append(Feature(each_token[1].join("_head"),score))
                #print "post "+each_token[1]
            if score<-0.1:
                negcount+=1
                f_list.append(Feature(each_token[1].join("_head"),score))
            #else: pass
    #f_list.append(Feature("poscount",poscount))
    #f_list.append(Feature("negcount",negcount))
    return f_list

def dependency_path(tweet_depparse):
    f_list=[]
    
    return f_list
 
