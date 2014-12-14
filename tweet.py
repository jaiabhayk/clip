import sys

debug = False
def normalize_tweet_token(token, posTag):
    if posTag in {'U', '@', 'D','$', 'U'}:
        return ''.join(['<', posTag,'>'])
    else:
        return token
    
class Tweet:
    """
    This object is used to store the tweets.
    featureList contains a list of objects of Feature class
    """
        
    def __init__(self, id=None, content=None, tokenized=None, lemmatized=None, dep_parse = None,
                 score=None, featureList=None, posTags=None):

        self.id = id
        if '\t' in content:
            print 'Unexpected tweet', content
            sys.exit()
        self.content = content
        tokenized_normalized = []
        for i in range(len(tokenized)):
            if debug:print 'token=', tokenized[i], 'tag=',posTags.name[i]
            tokenized_normalized.append(normalize_tweet_token(tokenized[i],posTags.name[i]))
        if debug:print 'tokenized_normalized=',tokenized_normalized
        
        self.tokenized = tokenized_normalized
        self.lemmatized = lemmatized
        self.dep_parse = dep_parse
        self.score = score
        self.featureList = featureList
        self.posTags = posTags

        
        


class Feature:
    """
    This class is used to represent features.
    value is always a float
    name is always a string
    """

    def __init__(self, name="", value=0):

        self.name = name
        self.value = value

    def __str__(self):
        return "%s : %s" % (self.name, self.value)
    
class PosTag:
    """
    This class is used to represent PosTag.
    value is always a float representing confidence
    name is always a string
    """

    def __init__(self, name=None, value=None):
        if len(name) !=len(value):
            print 'Unexpected input, the length of the pos tags and their confidence values should be same'
            sys.exit()

        self.name = name
        self.value = value

    def __str__(self):
        return "%s : %s" % (self.name, self.value)

