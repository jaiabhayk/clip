class Tweet:
    """
    This object is used to store the tweets.
    featureList contains a list of objects of Feature class
    """

    def __init__(self, id=None, content=None, score=0, featureList=None):

        self.id = id
        self.content = content
        self.score = score
        self.featureList = []


class Feature:
    """
    This class is used to represent features.
    value is always a float
    name is always a string
    """

    def __init__(self, name="", value=0):

        self.name = name
        self.value = value