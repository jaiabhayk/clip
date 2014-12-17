__author__ = 'yogarshi'

from tweet import *



def populate_nrc_dict(file):

    d = {}

    for each_line in file:
        x = each_line.strip().split()

        word = x[0]
        emotion = x[1]
        val = int(x[2])

        if word not in d:
            d[word] = {}

        d[word][emotion] = val


    return d

nrc_dict = populate_nrc_dict(open("NRCLexicon.txt", 'r'))
#print nrc_dict

def emotion_occurances(tweet_content):

    f_list = []
    emo_dict = {}

    emo_words = 0


    for each_word in tweet_content:
        emo_flag = False
        if each_word.lower() in nrc_dict:
            for each_emotion in nrc_dict[each_word.lower()]:
                if each_emotion not in emo_dict:
                    emo_dict[each_emotion] = 0
                if nrc_dict[each_word.lower()][each_emotion] == 1:
                    emo_dict[each_emotion] += 1
                    emo_flag = True
        if emo_flag:
            emo_words += 1

    #print emo_dict
    #if len(emo_dict) >0:
    #    print emo_dict
    for each in emo_dict:
        f_list += [Feature("nrcemo_"+each, emo_dict[each])]
    #f_list += [Feature("num_emo_words", emo_words)]
    return f_list


def combine_features(tweet):

    f_list = []

    f_list += emotion_occurances(tweet.lemmatized)


    return f_list