import sys

class Tweet:
    """
    This object is used to store the tweets.
    featureList contains a list of objects of Feature class
    """

    def __init__(self, id=None, content=None, tokenized=None, score=0, featureList=None, posTags=None):

        self.id = id
        if '\t' in content:
            print 'Unexpected tweet',content
            sys.exit()
        self.content = content
        self.tokenized = tokenized
        self.score = score
        self.featureList = featureList
        self.posTags = posTags;


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

