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

debug = False



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


def getSentiScoreFeatures(tweet):
    if debug:print '\ntweet\n', ' '.join(tweet.tokenized), '\n'
    f_list = []
    scores = Counter()
    no_of_sentences = 0
    
    
#     phrases = ['as_long_as_', '_as_long_as_', 'like_the_', '_like_the_', 'so_to_speak_', 
#                '_so_to_speak', '_so_to_speak_', 'so_', '_so_', '_since_', '_more_and_more_', '_more_than_'
#                , '_all_of_a_sudden_','all_of_a_sudden_',]
    

    
    phrases_sentences_map = {};
    tokenized_content = ('_'.join(tweet.tokenized)).lower()
    if debug:print tokenized_content
    phrase_found = 'sentence'
#     for phrase in phrases:
#         if phrase in tokenized_content:
#             phrase_found = phrase
#             break
#     if debug:print 'phrase found:-', phrase_found,'\n'
    
    total_senti_score = 0
    sent_score_count = 0
    
    for i in range(len(tweet.tokenized)):
        pos = (tweet.posTags.name[i]).lower()
        token = (tweet.tokenized[i]).lower()
        #token = stemmer.stem(token.decode('utf-8')).encode('utf-8')
        token = lemmatizer.lemmatize(token.decode('utf-8')).encode('utf-8')
        key = ''.join([token, "#", pos])
        # TODO don't consider stop words or a, as the etc ??
        # TODO use the lemma or stemmed word for score ??
        # first clean/normalize the words (ex:- you're etc)
        #TODO Apply on bigram as well or rather apply on phrases
        
        if pos in {',', '&','!','#', '@' }:
#             if debug: print 'Found end of sentence/phrase, key=',key
            if sent_score_count!=0:
                no_of_sentences+=1
                scores[ ''.join([phrase_found,'_',str(no_of_sentences)])] = sent_score_count
            sent_score_count = 0
            continue
            
        if key not in senti_word_dict:
            #TODO if not found then fallback to lemma or stemmed word
#             if debug:print 'No corresponding score found in the dictionary, skipping key=' , key
            continue
#         if debug:print '\nkey=', key, ':score=', senti_word_dict[key]
        score = senti_word_dict[key]
        

        if (score >0):
            scores['total_pos_senti_score'] += 1
#             if (score not in scores) or (score > scores['max_pos_senti_score']):
#                 scores['max_pos_senti_score'] = score
        elif score<0:
            scores['total_neg_senti_score']+=1
#             if (score not in scores) or (score < scores['max_neg_senti_score']):
#                 scores['max_neg_senti_score'] = score

        sent_score_count+=score     
#         scores[key] = score
        total_senti_score += score
        
    tweet_tokenized_lower = []
    for t in tweet.tokenized:
        tweet_tokenized_lower.append(t.lower())
        
    speial_hashtags = ['#sarcasm', '#not']   
    for speial_hashtag in speial_hashtags:
        if speial_hashtag in tweet_tokenized_lower:
            if debug:print 'found special hash tag flip the tweet score-', speial_hashtag, tweet.score
            total_senti_score = -1*total_senti_score
            break
    scores['total_senti_score'] += total_senti_score


     
    if debug: print '\n token:-', tweet.tokenized 
    if debug: print '\n pos:-', tweet.posTags
    if debug:print '\n All senti-word scores:- \n', scores
    for tag in scores:
        f_list.append(Feature(tag, scores[tag]))
    if debug:    
        print '\n senti-word Features List:-\n'
        for f in f_list: print f, '\t'
        print '\n===================-\n'

    return f_list




if __name__ == '__main__':
    pos = [];
    for keys in senti_word_dict:
        key = keys.split('#')
        key = key[1]
        if key not in pos:
            pos.append(key)
    print pos

    

    
