from nltk.stem.porter import PorterStemmer
import math

def normalize_token(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token.lower())

def calculate_tf_wt(term_freq):
    return math.log(term_freq, 10) + 1.0
