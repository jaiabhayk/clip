import sys
import time
from twokenize import *
from vw_interface import *
from tweet import *
from collections import Counter
from nltk.stem.porter import *
from nltk.stem.wordnet import WordNetLemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

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
        score = float(values[1]) 
        words[w] = score
        
    f.close()
    return words

senti_word_dict = populate_senti_word_dict('senti_wordnet_dictionary.txt')


def getSentiScoreFeatures(tweet):
    f_list = []
    scores = Counter()
    no_of_sentences = 0
    
    phrases_sentences_map = {};
    tokenized_content = ('_'.join(tweet.tokenized)).lower()
    if debug:print tokenized_content
    phrase_found = 'sentence'
    
    total_senti_score = 0
    sent_score_count = 0
    
    for i in range(len(tweet.tokenized)):
        pos = (tweet.posTags.name[i]).lower()
        token = (tweet.tokenized[i]).lower()
        token = lemmatizer.lemmatize(token.decode('utf-8')).encode('utf-8')
        key = ''.join([token, "#", pos])
        
        if pos in {',', '&', '!', '#', '@' }:
            if sent_score_count != 0:
                no_of_sentences += 1
                scores[ ''.join([phrase_found, '_', str(no_of_sentences)])] = sent_score_count
            sent_score_count = 0
            continue
            
        if key not in senti_word_dict:
            continue
        score = senti_word_dict[key]
        

        if (score > 0):
            scores['total_pos_senti_score'] += 1
        elif score < 0:
            scores['total_neg_senti_score'] += 1

        sent_score_count += score  
        total_senti_score += score
        
    tweet_tokenized_lower = []
    for t in tweet.tokenized:
        tweet_tokenized_lower.append(t.lower())
        
    speial_hashtags = ['#sarcasm', '#not']   
    for speial_hashtag in speial_hashtags:
        if speial_hashtag in tweet_tokenized_lower:
            # Found special hash tag flip the tweet score
            total_senti_score = -1 * total_senti_score
            break
    scores['total_senti_score'] += total_senti_score
    for tag in scores:
        f_list.append(Feature(tag, scores[tag]))
   
    return f_list

if __name__ == '__main__':
    pos = [];
    for keys in senti_word_dict:
        key = keys.split('#')
        key = key[1]
        if key not in pos:
            pos.append(key)
    print pos

    

    
