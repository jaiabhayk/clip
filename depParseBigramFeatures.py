from collections import Counter
__author__ = 'Abhay'

from tweet import *
import lexicon_features

from nltk.stem.porter import *
from nltk.stem.wordnet import WordNetLemmatizer
from depParseFeatures import *
import string

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

debug = True
def bigram_feature(tweet):
    f_list = []
    words, parents = unpack_dep_parse(tweet.dep_parse)
    if debug: print words, '\n', parents, '\n'
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
                
            feature_name = ''.join([feature_prefix, child, '_', parent])
            feature_name = string.replace(feature_name,':','<Colon>')
            feature_name = string.replace(feature_name,'|','<VertBar>')
            hist[feature_name] +=1
            
    for tag in hist: f_list.append(Feature(tag, hist[tag]))
    
    if debug:    
        print '\n The Dep Parse Bigram Fearures list:-\n'
        for f in f_list: print f, '\t'
        print '\n===================-\n'   
    
    f_list1 = []
    f_list1.append(Feature('dep_bigram_feature_it\'s_the ? 6.5 . , _| '' # & <dot> thre-year @ " |',1))
    return f_list



def combine_features(tweet):
    f_list = []
    f_list = bigram_feature(tweet)
    return f_list

