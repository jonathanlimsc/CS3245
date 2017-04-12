import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer

def process_raw_to_tokens(content):
    """
    Given raw text content, we perform the following operations:
    casefolding, tokenizing, stemming, stripping punctuation
    """
    # print "processing:",
    # print content
    tokenizer = RegexpTokenizer(r'\w+')
    stemmer = PorterStemmer()

    tokens = []
    sentences = nltk.sent_tokenize(content)
    for sentence in sentences:
        words = tokenizer.tokenize(sentence.lower())
        processed = []
        for word in words:
            try:
                stemmed_word = stemmer.stem(word)
                processed.append(stemmed_word)
            except:
                processed.append(word)
        # processed = [self.stemmer.stem(word) for word in words if len(word) >= 2]
        tokens.extend(processed)
    return tokens
