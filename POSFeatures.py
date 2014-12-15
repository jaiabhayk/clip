__author__ = 'yogarshi'


from tweet import *

def POS_unigrams(pos_sequence):

    f_list = []
    pos_dict = {}
    #print pos_sequence
    for each in pos_sequence:
        #print each
        if each not in pos_dict:
            pos_dict[each] = 0
        pos_dict[each] +=1

    #print pos_dict
    #f_list = sorted([Feature(x,pos_dict[x]) for x in pos_dict ], key=lambda x : x.value, reverse = True)
    if '!' in pos_dict:
        f_list += [Feature("num_exclaim", pos_dict['!'] )]
    if 'E' in pos_dict:
        f_list += [Feature("num_emo", pos_dict['E'] )]
    #if 'A' in pos_dict:
    #    f_list += [Feature("num_adj", pos_dict['A'] )]
    if 'R' in pos_dict:
        f_list += [Feature("num_adv", pos_dict['R'] )]

    #f_list = Feature("num_adverbs", )

    return f_list



def POS_bigrams(pos_sequence):

    f_list = []
    bi_dict = {}
    for i in range(len(pos_sequence)-1):
        #if pos_sequence[i].isalnum() and pos_sequence[i+1].isalnum():
        t = pos_sequence[i] + '_' + pos_sequence[i+1]
        if t not in bi_dict:
            bi_dict[t] = 0
        bi_dict[t] += 1

    for each in bi_dict:
        f_list.append(Feature(each, bi_dict[each]))
    return f_list

def combine_features(tweet):


    f_list = []
    #print tweet.posTags.name
    f_list += POS_unigrams(tweet.posTags.name)
    #f_list += POS_bigrams(tweet.posTags.name)


    return f_list