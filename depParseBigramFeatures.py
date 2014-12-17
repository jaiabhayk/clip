from collections import Counter
__author__ = 'Abhay'

from tweet import *
import lexicon_features

from nltk.stem.porter import *
from nltk.stem.wordnet import WordNetLemmatizer
from depParseFeatures import *
import string
import senti_wordnet_features  



stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

senti_word_dict = senti_wordnet_features.populate_senti_word_dict('senti_wordnet_dictionary.txt')
tags=['n','v','a','r']

debug = False
def bigram_feature(tweet):
    f_list = []
    words, parents = unpack_dep_parse(tweet.dep_parse)
    if debug: print words, '\n', parents, '\n', 'pos=', tweet.posTags.name
    feature_prefix = 'dep_bigram_feature_'
    hist = Counter()
    for i in range(len(words)):
        #TODO why we need to put parents[i]>len(words), need to verify
        if (parents[i] ==-1):
            continue
        else:
            pos = tweet.posTags.name[i] 
            if pos in {'U', '@', 'D','$', 'U'}:
                child =  ''.join(['<', pos,'>'])
            else:
                child = (words[i]).lower()
                
           
            parentPos = tweet.posTags.name[parents[i]-1]
            if parentPos in {'U', '@', 'D','$', 'U'}:
                parent =  ''.join(['<', parentPos,'>'])
            else:
                parent = (words[parents[i]-1]).lower()
            
            child = lemmatizer.lemmatize(child.decode('utf-8')).encode('utf-8')  
            parent = lemmatizer.lemmatize(parent.decode('utf-8')).encode('utf-8')
            
            feature_name = ''.join([feature_prefix, child, '_', parent])
            feature_name = string.replace(feature_name,':','<Colon>')
            feature_name = string.replace(feature_name,'|','<VertBar>')
            hist[feature_name] +=1
            
    for tag in hist: f_list.append(Feature(tag, hist[tag]))
    
    if debug:    
        print '\n The Dep Parse Bigram Fearures list:-\n'
        for f in f_list: print f, '\t'
        print '\n===================-\n'  
    return f_list

def bigram_feature_with_polarity(tweet):
    f_list = []
    words, parents = unpack_dep_parse(tweet.dep_parse)
    if debug: print words, '\n', parents, '\n','pos=', tweet.posTags.name
    feature_prefix = 'dep_bigram_feature_with_polarity_'
    hist = Counter()
    for i in range(len(words)):
        #TODO why we need to put parents[i]>len(words), need to verify
        if (parents[i] ==-1):
            continue
        else:
            pos = tweet.posTags.name[i]
            
            if pos in {'U', '@', 'D','$', 'U'}:
                child =  ''.join(['<', pos,'>'])
            else:
                child = (words[i]).lower()
                
           
            parentPos = tweet.posTags.name[parents[i]-1]
            if parentPos in {'U', '@', 'D','$', 'U'}:
                parent =  ''.join(['<', parentPos,'>'])
            else:
                parent = (words[parents[i]-1]).lower()
            
            child,child_score = getNameScorePair(child,pos)
            parent,parent_score = getNameScorePair(parent,parentPos)
            if debug: print 'child-', child, ' score-', child_score
            if debug: print 'parent-', parent, ' score-', parent_score
            if child_score ==0 or parent_score ==0:
                continue
            #TODO should I remove the #postag from the word names ?
            feature_name = ''.join([feature_prefix, child, '_', parent])
            feature_name = string.replace(feature_name,':','<Colon>')
            feature_name = string.replace(feature_name,'|','<VertBar>')
            hist[feature_name] += child_score*parent_score
            
    for tag in hist: f_list.append(Feature(tag, hist[tag]))
    
    if debug:    
        print '\n The Dep Parse Bigram Polarity Fearures list:-\n'
        for f in f_list: print f, '\t'
        print '\n===================-\n'  
    return f_list

def getNameScorePair(word,pos):
     token_word = word.lower()
     pos=pos.lower()
     token_lemma = lemmatizer.lemmatize(word.lower().decode('utf-8')).encode('utf-8')
     token_stem = stemmer.stem(word.lower().decode('utf-8')).encode('utf-8')
     check_list=[''.join([token_word,'#',pos]),''.join([token_lemma,'#',pos]),''.join([token_stem,'#',pos]),''.join([token_word,'#','n']),''.join([token_word,'#','v']),''.join([token_word,'#','a']),''.join([token_word,'#','r']),''.join([token_lemma,'#','n']),''.join([token_lemma,'#','v']),''.join([token_lemma,'#','a']),''.join([token_lemma,'#','r']),''.join([token_stem,'#','n']),''.join([token_stem,'#','v']),''.join([token_stem,'#','a']),''.join([token_stem,'#','r'])]

     key=''.join([token_word,'#',pos])
     score = 0
     for i in check_list:
         if i in senti_word_dict:
              key=i
              break
         else: continue

     if key not in senti_word_dict:
         score = 0
     else:
         score = senti_word_dict[key]
     if score>0:
         score =1
     elif score <0:
        score =-1
         
     return key,score
    


def combine_features(tweet):
    f_list = []
    f_list += bigram_feature(tweet)
    f_list += bigram_feature_with_polarity(tweet)
    return f_list

