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
    # Since cleaner already has taken care of punctuation, we don't need to find the sentences
    # sentences = nltk.sent_tokenize(content)
    # print "Num of sentences: " + str(len(sentences))
    # for sentence in sentences:
    words = tokenizer.tokenize(content.lower())
    processed = []
    for word in words:
        try:
            stemmed_word = stemmer.stem(word)
            processed.append(stemmed_word)
        except:
            processed.append(word)
    # processed = [self.stemmer.stem(word) for word in words if len(word) >= 2]
    tokens.extend(processed)
    print "Length of tokens: " + str(len(tokens))

    return tokens
