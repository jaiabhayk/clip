__author__ = 'yogarshi'

from tweet import *
import lexicon_features

from nltk.stem.porter import *
from nltk.stem.wordnet import WordNetLemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def unpack_dep_parse(dep_parse):

    words = [x[1] for x in dep_parse]
    parents = [int(x[6]) for x in dep_parse]

    return words, parents

def detect_sentences(dep_parse):

    f_list = []

    words, parents = unpack_dep_parse(dep_parse)
    to_sep = [True for x in parents]

    sent_sets = []
    set_dict = {}
    #detect the roots
    roots = []
    for i in range(len(parents)):
        if parents[i] == 0:
            roots.append(i)
        if parents[i] == -1:
            to_sep[i] = False

    #create sentences sets
    for i in range(len(roots)):

        sent_sets.append(set())
        sent_sets[-1].add(roots[i])
        set_dict[roots[i]] = i
        to_sep[roots[i]] = False

    #assign words to sentence sets - horribly naive, must be fixed
    while True in to_sep:
        #print to_sep
        #print parents
        for i in range(len(parents)):
            if to_sep[i]:
                curr_par = parents[i]-1
                if curr_par in set_dict:
                    assign_to = set_dict[curr_par]
                    sent_sets[assign_to].add(i)
                    set_dict[i] = assign_to
                    to_sep[i] = False

    #print sent_sets

    ret = [[words[y] for y in sorted(x)] for x in sent_sets]

    #print ret
    return ret
    #print roots

    #f_list += [Feature("num_sentences_dp", len(roots))]

    #f_list += list(set([Feature("root_word_" + words[x].lower(), 1) for x in roots]))

    #return f_list


def emotion_occurances(tweet_content):

    f_list = []
    emo_dict = {}

    emo_words = 0


    for each_word in tweet_content:
        emo_flag = False
        try:
            word = lemmatizer.lemmatize(each_word.lower())
        except UnicodeDecodeError:
            word = each_word.lower()
        if each_word.lower() in lexicon_features.nrc_dict:
            for each_emotion in lexicon_features.nrc_dict[each_word.lower()]:
                x = lexicon_features.nrc_dict[each_word.lower()][each_emotion]
                if x == 1:
                    if each_emotion not in emo_dict:
                        emo_dict[each_emotion] = 0
                    emo_dict[each_emotion] += 1
                    emo_flag = True
        elif word in lexicon_features.nrc_dict:
            for each_emotion in lexicon_features.nrc_dict[word]:
                x = lexicon_features.nrc_dict[word][each_emotion]
                if x == 1:
                    if each_emotion not in emo_dict:
                        emo_dict[each_emotion] = 0
                    emo_dict[each_emotion] += 1
                    emo_flag = True
        if emo_flag:
            emo_words += 1

    #print emo_dict
    #if len(emo_dict) >0:
    #    print emo_dict
    #for each in emo_dict:
    #    f_list += [Feature("nrcemo_"+each, emo_dict[each])]
    #f_list += [Feature("num_emo_words", emo_words)]
    #return f_list
    return emo_dict


def sent_emo_occurance(sentences):

    emo_dicts = []
    for each_sent in sentences:
        emo_dicts.append(emotion_occurances(each_sent))

    #print emo_dicts

    return emo_dicts


def multi_sentence(sentences):

    emo_dicts = sent_emo_occurance(sentences)
    f_list  = []
    neg_list = ['anger', 'disgust', 'fear', 'sadness', 'negative']
    pos_list = ['anticipation', 'joy', 'surprise', 'trust', 'positive']
    pos_flag = False
    neg_flag = False
    pos_count = 0
    neg_count = 0
    count = 1
    for each_dict in emo_dicts:
        pre = "sent" + str(count) + '_'
        for each_emo in each_dict:
            if each_emo in pos_list:
                f_list += [Feature(pre+each_emo,each_dict[each_emo])]
                pos_flag = True
                pos_count += 1
            if each_emo in neg_list:
                f_list += [Feature(pre+each_emo,each_dict[each_emo])]
                neg_flag = True
                neg_count += 1
        count += 1

    if pos_flag and neg_flag:
        f_list += [Feature("contradictory_emo_posneg", 1)]

    return f_list



def combine_features(tweet):

    f_list = []
    sentences = detect_sentences(tweet.dep_parse)

    f_list += multi_sentence(sentences)

    return f_list

