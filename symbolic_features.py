__author__ = 'rashmi'

from tweet import *

def smiley_count(tweet_content):
    smile = [':)', ':-)','^_^']
    sad = [':(', ':-(']
    kidding = [':P', ':-P']
    wink = [';)',';-)']
    surprize = [':O',':-O']
    laugh = [':D', ':-D',":'D",":'-D"]
    cry = [":'(",":'-(", ":*(", ":*-(",":{",":["]
    smilecry = [":')",":'-)"]
    heart = ["<3"]
    kiss = [":*",":X",":-*",":-X"]
    indifference = [":|",":-|", "-_-"]
    count = 0
    smiley_dict={"smile":0,"sad":0,"kidding":0, "wink":0, "surprize":0,"laugh":0,"cry":0,"smilecry":0,"heart":0,"kiss":0,"indifference":0}
 
    f_list=[]
    for each_token in tweet_content:
        if each_token.upper() in smile:
            smiley_dict["smile"]+=1
        if each_token.upper() in sad:
            smiley_dict["sad"]+=1
        if each_token.upper() in kidding:
            smiley_dict["kidding"]+=1
        if each_token.upper() in wink:
            smiley_dict["wink"]+=1
        if each_token.upper() in surprize:
            smiley_dict["surprize"]+=1
        if each_token.upper() in laugh:
            smiley_dict["laugh"]+=1
        if each_token.upper() in cry:
            smiley_dict["cry"]+=1
        if each_token.upper() in smilecry:
            smiley_dict["smilecry"]+=1
        if each_token.upper() in heart:
            smiley_dict["heart"]+=1
        if each_token.upper() in kiss:
            smiley_dict["kiss"]+=1
        if each_token.upper() in indifference:
            smiley_dict["indifference"]+=1

    for each_item in smiley_dict:
        f_list.append(Feature(each_item,smiley_dict[each_item]))  

    return f_list
