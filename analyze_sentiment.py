"""
This is the code that has to be run.
"""

#from weka_interface import *
import sys
import time
from twokenize import *
from vw_interface import *
from tweet import *
from abhay_features import *
from rashmi_features import *
from yogarshi_features import *
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer


def read_tweets(filename):
    """
    Read the tweet data from a file and store in tweet objects. Tokenize using Twitter tokenizer
    :param filename:
    :return:
    """
    tweet_list = list()
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()

    f = open(filename, 'r')
    ids = {}
    scores = {}
    
    for line in f.readlines():
        values = line.split("\t")
        if len(values) > 3:
            print 'Unexpected tweet'
            sys.exit()
        ids[values[2] ]=values[0]
        scores[values[2]] = values[1]
    f.close()
    
    #filename.posTagged is the file after running posTagger
    filename_posTagged = ''.join([filename,'.posTagged'])
    raw_tweet_file = ''.join([filename,'.rawTweets'])

    #Also read the dependency parse from filename.depParse
    filename_depParsed = ''.join([filename,'.depParse'])

    ###TODO: Dep parse file has all the information you need. Can delete stuff where we read pos tagged file
    ###TODO: and get tags from dep parse
    
    command =  ''.join(['sh ark-tweet-nlp-0.3.2/runTagger.sh ',  raw_tweet_file, '  > ',  filename_posTagged])
    
    DataDir = filename.split('/')
    if len(DataDir) ==1: 
        DataDir = './'
    else:
        DataDir = DataDir[len(DataDir)-2]
  
    if filename_posTagged.split('/')[-1] in os.listdir(DataDir):
        print 'File ', filename_posTagged.split()[-1] , 'Already Present, Skipping Recreation....' 
    else:
        print 'File ', filename_posTagged.split()[-1] , 'Not Present, Creating it....'       
        if (os.system(command) !=0):
            print 'Error while running the command, ',  command
            sys.exit()
    
    
    f = open(filename_posTagged, 'r')
    f_prime = open(filename_depParsed, 'r')
    for line in f.readlines():
        values = line.split("\t")
        if len(values) != 4:
            print 'Unexpected tweet'
            sys.exit()
        
        text = values[3]
        id = ids[text]
        tokenize_text = values[0].split(' ')

        try:
            lemmatize_text = [lemmatizer.lemmatize(x) for x in tokenize_text]
            lemmatize_text = [lemmatizer.lemmatize(x) for x in tokenize_text]
        except UnicodeDecodeError:
            lemmatize_text = tokenize_text

        dep_parse = []
        for x in range(len(tokenize_text)):
            dep_parse.append(f_prime.readline().strip().split())
        f_prime.readline()
        #print dep_parse

        score = scores[text]
        posTag = PosTag(values[1].split(),values[2].split())
        tweet_list.append(Tweet(id, text, tokenize_text, lemmatize_text, dep_parse, round(float(score),2), [], posTag))
    f.close()
    f_prime.close()

    return tweet_list


def get_features(tweet):
    # ## TODO: Using a toy feature right now to check all other parts of the code. This function will call all other
    # ## TODO: feature extraction functions

    feature_list = []
    feature_list += getAbhayFeatures(tweet)
    feature_list += getRashmiFeatures(tweet)
    feature_list += getYogarshiFeatures(tweet)

    return feature_list


def main(argv):

    if len(argv) > 2:
        print "Incorrect number of arguments. Usage python analyze_sentiment.py <training_data_file> [<test_data_file>]"
        sys.exit()

    # ##TODO: Use argparse to handle command line arguments

    train_file_raw = argv[0]
    test_file_raw = None
    folds = 5  # ## TODO: Make this a command line parameter

    training_file = "TrainingSet.vw"
    test_file = "TestSet.vw"


    # Check if testfile has been provided
    if len(argv) == 2:
        test_file_raw = argv[1]



    # Read the tweets and store in a tokenized form
    training_tweet_list = read_tweets(train_file_raw)
    test_tweet_list = []
    if test_file_raw is not None:
        test_tweet_list = read_tweets(test_file_raw)


    # Assemble the features
    for each_tweet in training_tweet_list:
        each_tweet.featureList = get_features(each_tweet)
        each_tweet.featureList.append(Feature("tweet_id", each_tweet.id))

    if test_file_raw is not None:
        for each_tweet in test_tweet_list:
            each_tweet.featureList = get_features(each_tweet)
            each_tweet.featureList.append(Feature("tweet_id", each_tweet.id))
            
    #increase Negative tweet size in training only
    new_training_tweet_list = list(training_tweet_list)
    print 'new_training_tweet_list_size-before' , len(new_training_tweet_list)
    for each_tweet in training_tweet_list:
        if each_tweet.score >0:
            for i in range(2):new_training_tweet_list.append(each_tweet)
            
    #training_tweet_list = new_training_tweet_list
    print 'new_training_tweet_list_size-after' , len(new_training_tweet_list)        


    # Create training and testing files
    #create_arff_file(training_tweet_list, training_file, test_tweet_list, test_file)
    write_to_file(training_tweet_list, training_file)
    write_to_file(test_tweet_list, test_file)


    #Do vw stuff
    #start_time = time.time()

    print "#############################"
    print "Doing Kfold Cross validation"
    print "#############################"
    print
    k_fold(training_tweet_list, 10)


    print "#############################"
    print "Starting training...."
    print "#############################"
    print
    train_vw(training_file)

    print
    print "#############################"
    print "Starting testing...."
    print "#############################"
    print
    test_vw(test_file)


    print
    print "#############################"
    print "Generating Predictions.txt for error analysis..."
    print "#############################"
    print
    map_predictions(test_tweet_list, -1)



if __name__ == "__main__":
    command = "rm *.cache"
    os.system(command)
    command = "rm TestSet.vw TrainingSet.vw model.vw model.vw predictions.vw"
    os.system(command)


    if len(sys.argv) == 1:
        print 'No Arguments passed, using default'
        main(['DataCopy1/TrainingSetCleaned.txt', 'DataCopy1/TrialSetCleaned.txt'])
    else:
        main(sys.argv[1:])
