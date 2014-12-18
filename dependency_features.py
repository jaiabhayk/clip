__author__ = 'rashmi'

from tweet import *
from senti_wordnet_features import *
from nltk.stem.porter import *
from nltk.stem.wordnet import WordNetLemmatizer
import string
import lexicon_features
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

senti_word_dict = populate_senti_word_dict('senti_wordnet_dictionary.txt')
tags=['n','v','a','r']

def root_count(tweet_depparse):
    f_list=[]
    poscount=0
    negcount=0

    for each_token in tweet_depparse:
        if each_token[6] == '0':
            pos = each_token[3].lower()
            token_word = each_token[1].lower()
            token_lemma = lemmatizer.lemmatize(each_token[1].lower().decode('utf-8')).encode('utf-8')
            token_stem = stemmer.stem(each_token[1].lower().decode('utf-8')).encode('utf-8')
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
            
            if score>0.1:
                poscount+=1
                feature_name=each_token[1].join("_head")
                feature_name = string.replace(feature_name,':','<Colon>')
                feature_name = string.replace(feature_name,'|','<VertBar>')
                f_list.append(Feature(each_token[1].join("_head"),score))

            if score<-0.1:
                negcount+=1
                feature_name=each_token[1].join("_head")
                feature_name = string.replace(feature_name,':','<Colon>')
                feature_name = string.replace(feature_name,'|','<VertBar>')
                f_list.append(Feature(each_token[1].join("_head"),score))
    #f_list.append(Feature("poscount",poscount))
    #f_list.append(Feature("negcount",negcount))
    return f_list

def senti(word,pos):
     token_word = word.lower()
     pos=pos.lower()
     token_lemma = lemmatizer.lemmatize(word.lower().decode('utf-8')).encode('utf-8')
     token_stem = stemmer.stem(word.lower().decode('utf-8')).encode('utf-8')
     check_list=[''.join([token_word,'#',pos]),''.join([token_lemma,'#',pos]),''.join([token_stem,'#',pos]),''.join([token_word,'#','n']),''.join([token_word,'#','v']),''.join([token_word,'#','a']),''.join([token_word,'#','r']),''.join([token_lemma,'#','n']),''.join([token_lemma,'#','v']),''.join([token_lemma,'#','a']),''.join([token_lemma,'#','r']),''.join([token_stem,'#','n']),''.join([token_stem,'#','v']),''.join([token_stem,'#','a']),''.join([token_stem,'#','r'])]

     key=''.join([token_word,'#',pos])
     for i in check_list:
         if i in senti_word_dict:
              key=i
              break
         else: continue

     if key not in senti_word_dict:
         return 0
     else:
         score = senti_word_dict[key]
         return score


def dependency_path(tweet_depparse):
    f_list=[]
    path=[]
    score=0
    for token1 in tweet_depparse:
        path=[]
        score=0
        if token1[6]=='0':
            path.append(token1[1].lower())
            score+=senti(token1[1],token1[3])
            for token2 in tweet_depparse:
                if token2[6]==token1[0]: 
                    path.append(token2[1].lower())
                    score+=senti(token2[1],token2[3])
                    for token3 in tweet_depparse:
                        if token3[6]==token2[0]:
                            #final='-'.join(path)+"-"token3[1]
                            path.append(token3[1].lower())
                            score+=senti(token3[1].lower(),token3[3])
                            feature_name='-'.join(path)
                            feature_name = string.replace(feature_name,':','<Colon>')
                            feature_name = string.replace(feature_name,'|','<VertBar>')
                            f_list.append(Feature(feature_name,score))
                            #print '-'.join(path)
                            path.remove(token3[1].lower())
                            score-=senti(token3[1],token3[3])
                    path.remove(token2[1].lower())
                    score-=senti(token2[1],token2[3])
            path.remove(token1[1].lower())
            score-=senti(token1[1],token1[3])
    return f_list
   
def dependency_pathdfs(tweet_depparse):
    f_list=[]
    path=[]
    score=0
    children_dict={}
    leaf_list=[]
    for token in tweet_depparse:
        for token_child in tweet_depparse:
            if token_child[6]==token[0]:
                children_dict.setdefault(token[0],[]).append(token_child[0])
            #print children_dict[token[0]]
    for token in tweet_depparse:
        if token[0] not in children_dict.keys():
            leaf_list.append(token[0])
    countpos=0
    countneg=0
    countmix=0
    for leaf in leaf_list:
        path=[]
        allpos=0
        allneg=0
        
        path.append(tweet_depparse[int(leaf)-1][1])
        parent=int(leaf)
        #print tweet_depparse[int(leaf)-1][6]
       
        while int(tweet_depparse[parent-1][6])!=0 and int(tweet_depparse[parent-1][6])!=-1:
            #print tweet_depparse[parent-1][6]
            parent=int(tweet_depparse[parent-1][6])
            path.append(tweet_depparse[parent-1][1])
        for item in path:
            token_word = item.lower()
            token_lemma = lemmatizer.lemmatize(item.lower().decode('utf-8')).encode('utf-8')
            token_stem = stemmer.stem(item.lower().decode('utf-8')).encode('utf-8')
            if token_word not in lexicon_features.nrc_dict: item=token_lemma
            if item not in lexicon_features.nrc_dict: item=token_stem
            if item not in lexicon_features.nrc_dict: continue
            if lexicon_features.nrc_dict[item]['positive']==1: allpos+=1
            if lexicon_features.nrc_dict[item]['negative']==1: allneg+=1
        if allpos>0 and allneg==0: countpos+=1
        if allpos==0 and allneg>0: countneg+=1
        if allpos>0 and allneg>0: countmix+=1
        feature_name ='-'.join(path)
        feature_name = string.replace(feature_name,':','<Colon>')
        feature_name = string.replace(feature_name,'|','<VertBar>')
        #f_list.append(Feature(feature_name,1))
        #print '-'.join(path)
    f_list.append(Feature('allpos',countpos))
    f_list.append(Feature('allneg',countneg))
    f_list.append(Feature('mix',countmix))
    
    return f_list
