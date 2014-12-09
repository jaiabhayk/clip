__author__ = 'yogarshi'
"""
Mixed bag of features
"""

from tweet import *

def num_capital(tweet_content):

    val = 0
    for each_token in tweet_content:
        if each_token.isupper():
            val += 1

    return [Feature("num_capital", val)]


def add_bigrams(tweet_content):

    f_list = []
    bi_dict = {}
    for i in range(len(tweet_content)-1):
        if tweet_content[i].isalnum() and tweet_content[i+1].isalnum():
            t = tweet_content[i].lower() + '_' + tweet_content[i+1].lower()
            if t not in bi_dict:
                bi_dict[t] = 0
            bi_dict[t] +=1

    for each in bi_dict:
        f_list.append(Feature(each, bi_dict[each]))
    return f_list


def add_trigrams(tweet_content):

    f_list = []
    tri_dict = {}
    for i in range(len(tweet_content)-2):
        if tweet_content[i].isalnum() and tweet_content[i+1].isalnum() and tweet_content[i+2].isalnum():
            t = tweet_content[i].lower() + '_' + tweet_content[i+1].lower() + '_' + tweet_content[i+2].lower()
            if t not in tri_dict:
                tri_dict[t] = 0
            tri_dict[t] += 1

    for each in tri_dict:
        f_list.append(Feature(each, tri_dict[each]))
    return f_list

def is_retweet(tweet_content):

    if tweet_content[0] == "RT":
        return [Feature("is_retweet", 1)]
    else:
        return [Feature("is_retweet", 0)]


def num_at_mentions(tweet_content):
    val = 0
    for each_token in tweet_content:
        if each_token[0] == '@':
            val += 1

    return [Feature("num_at_mentions", val)]

def get_n_grams(word,n):
    n_grams = {}
    for i in range(len(word)-(n-1)):
        n_gram = word[i:i+n]
        if n_gram not in n_grams:
            n_grams[n_gram] = 0
        n_grams[n_gram] += 1

    return sorted([(n_grams[x], x) for x in n_grams])


def character_n_grams(tweet_content):
    f_list = []
    for each_word in tweet_content:
        if each_word.isalpha():
            #bigrams = get_n_grams(each_word.lower(),)
            trigrams = get_n_grams(each_word.lower(),3)
            #for each_bigram in bigrams:
            #    f_list.append(Feature(each_bigram[1], each_bigram[0]))
            for each_trigram in trigrams:
                f_list.append(Feature(each_trigram[1], each_trigram[0]))

    return f_list


def cf_terms(tweet_content):
    cf_list = ['about', 'almost', 'although', 'approximately', 'around', 'but', 'close', 'even', 'hence', 'herefore',
               'however', 'just', 'less', 'merely', 'more', 'most', 'near', 'nearly', 'nevertheless', 'nigh', 'no',
               'non', 'nonetheless', 'not', 'notwithstanding', 'now', 'only', 'roughly', 'simply', 'so', 'some',
               'still', 'then', 'thence', 'therefore', 'though', 'thus', 'virtually', 'well-nigh', 'withal', 'yet']

    val = {}
    f_list  =[]
    for each_word in tweet_content:
        if each_word.lower() in cf_list:
            if each_word.lower() not in val:
                val[each_word.lower()] = 0
            val[each_word.lower()] += 1

    for each_word in val:
        f_list.append(Feature(each_word, val[each_word]))

    return f_list


def slang_word(tweet_content):


    slang_list = ['fuck', 'fucking', 'fucks', 'fucked', 'shit', 'bitch', 'bitches']
    count = 0
    for each_word in tweet_content:
        if each_word.lower() in slang_list :
            count += 1
            #return [Feature("fuck", 1)]
    return [Feature("fuck", count)]


def has_words(tweet_content):
    word_list = ['irony', 'sarcasm', 'literally', 'definitely', 'lol', 'lmao', 'lmfao', 'jk', 'proverbial', 'virtually', 'funny']#,"so to speak"]

    val = {}
    f_list  =[]
    for each_word in tweet_content:
        if each_word.lower() in word_list:
            if each_word.lower() not in val:
                val[each_word.lower()] = 0
            val[each_word.lower()] += 1

    for each_word in val:
        f_list.append(Feature(each_word, val[each_word]))

    return  f_list



def combine_features(tweet_content):

    f_list = []

    f_list += num_capital(tweet_content)
    f_list += add_bigrams(tweet_content)
    f_list += add_trigrams(tweet_content)
    f_list += is_retweet(tweet_content)
    f_list += num_at_mentions(tweet_content)
    #f_list += character_n_grams(tweet_content)
    f_list += cf_terms(tweet_content)
    f_list += slang_word(tweet_content)
    f_list += has_words(tweet_content)

    return f_list





