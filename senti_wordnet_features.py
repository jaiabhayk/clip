import sys
import time
from twokenize import *
from vw_interface import *
from tweet import *
from collections import Counter

debug = True

def populate_senti_word_dict(filename):
    """
    populated the sentiment wordnet dictionary
    """
    words = {};
    f = open(filename, 'r')
    for line in f.readlines():
        values = line.split("=");
        if len(values) > 2:
            print 'Unexpected entry'
            sys.exit()
            
        w = values[0]
        # TODO double not in python but in numpy should be use numpy
        score = float(values[1]) 
        words[w] = score
        
    f.close()
    return words

senti_word_dict = populate_senti_word_dict('senti_wordnet_dictionary.txt')

def getSentiScoreFeatures(tweet_content):
    if debug:print '\ntweet\n', ' '.join(tweet_content), '\n'
    f_list = []
    scores = Counter()
    pos_map = getPOStag(tweet_content)
    for token in tweet_content:
        pos = pos_map[token]
        key = ''.join([token.lower(), "#", pos])
        # TODO don't consider stop words or a, as the etc ??
        # TODO use the lemma or stemmed word for score ??
        # first clean/normalize the words (ex:- you're etc)
        #TODO Apply on bigram as well or rather apply on phrases
        if key not in senti_word_dict:
            if debug:print 'No corresponding score found in the dictionary, skipping key=' , key
            continue
        if debug:print '\nkey=', key, ':score=', senti_word_dict[key]
        score = senti_word_dict[key]
        if (score >0.1):
#             scores['total_max_pos_senti_score'] += score
            if (score not in scores) or (score > scores['max_pos_senti_score']):
                scores['max_pos_senti_score'] = score
        elif score<-0.1:
#             scores['total_max__neg_senti_score']=score
            if (score not in scores) or (score < scores['max_neg_senti_score']):
                scores['max_neg_senti_score'] = score
            
#         scores[key] += score
#         scores['total_senti_score'] += score
     
    if debug:print '\n All senti-word scores:- \n', scores
    for tag in scores:
        f_list.append(Feature(tag, scores[tag]))
    if debug:    
        print '\n senti-word Features List:-\n'
        for f in f_list: print f, '\t'
        print '\n===================-\n'

    return f_list



def getPOStag(content):
    """ TODO
    Implement this to get the POS tag of the word (noun, verb etc.)
    """ 
    pos_map = {};
    possible_pos = ['n', 'v','a',  'r']
    
    for token in content:
        # TODO remove this work-around to know the pos
        # default is noun, n stands for noun (similar to wordnet 3.0
        
        pos_map[token] = 'n'  
        for pos in possible_pos:
            key = ''.join([token.lower(), "#", pos])
            if key not in senti_word_dict:
#                 if debug:print 'pos tagger, key NOT found in senti_word_dict-',key
                continue
            else:
#                 if debug:print 'pos tagger, key found in senti_word_dict, exit-',key 
                pos_map[token] = pos  
                break;
    return pos_map

if __name__ == '__main__':
    pos = [];
    for keys in senti_word_dict:
        key = keys.split('#')
        key = key[1]
        if key not in pos:
            pos.append(key)
    print pos

    

    
