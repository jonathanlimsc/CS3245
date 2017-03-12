from nltk.stem.porter import PorterStemmer

def normalize_token(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token.lower())
