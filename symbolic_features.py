__author__ = 'rashmi'

from tweet import *

def smiley_count(tweet_content):
    smiley_smile = [':)', ':-)','^_^']
    smiley_sad = [':(', ':-(']
    smiley_kidding = [':P', ':-P']
    smiley_wink = [';)',';-)']
    smiley_surprize = [':O',':-O']
    smiley_laugh = [':D', ':-D',":'D",":'-D"]
    smiley_cry = [":'(",":'-(", ":*(", ":*-(",":{",":["]
    smiley_smilecry = [":')",":'-)"]
    smiley_heart = ["<3"]
    smiley_kiss = [":*",":X",":-*",":-X"]
    smiley_indifference = [":|",":-|", "-_-"]
    count = 0
    smiley_dict={"smiley_smile":0,"smiley_sad":0,"smiley_kidding":0, "smiley_wink":0, "smiley_surprize":0,"smiley_laugh":0,"smiley_cry":0,"smiley_smilecry":0,"smiley_heart":0,"smiley_kiss":0,"smiley_indifference":0}
 
    f_list=[]
    for each_token in tweet_content:
        if each_token.upper() in smiley_smile:
            smiley_dict["smiley_smile"]+=1
        if each_token.upper() in smiley_sad:
            smiley_dict["smiley_sad"]+=1
        if each_token.upper() in smiley_kidding:
            smiley_dict["smiley_kidding"]+=1
        if each_token.upper() in smiley_wink:
            smiley_dict["smiley_wink"]+=1
        if each_token.upper() in smiley_surprize:
            smiley_dict["smiley_surprize"]+=1
        if each_token.upper() in smiley_laugh:
            smiley_dict["smiley_laugh"]+=1
        if each_token.upper() in smiley_cry:
            smiley_dict["smiley_cry"]+=1
        if each_token.upper() in smiley_smilecry:
            smiley_dict["smiley_smilecry"]+=1
        if each_token.upper() in smiley_heart:
            smiley_dict["smiley_heart"]+=1
        if each_token.upper() in smiley_kiss:
            smiley_dict["smiley_kiss"]+=1
        if each_token.upper() in smiley_indifference:
            smiley_dict["smiley_indifference"]+=1

    for each_item in smiley_dict:
        f_list.append(Feature(each_item,smiley_dict[each_item]))  

    return f_list
