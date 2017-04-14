import getopt
import sys
import math
import json
import cPickle
import nltk
import os
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import time

from posting import *
from cleaner import *
from utils import process_raw_to_tokens

class Indexer(object):

    def __init__(self, dictionary_fname, posting_fname):
        self.dict = {}
        self.numDocs = 0
        self.stemmer = PorterStemmer()
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.posting_fname = posting_fname
        self.dictionary_fname = dictionary_fname

    def addDoc(self, docObj):
        content = docObj['content']
        docId = docObj['docId']
        start_time = time.time()
        terms = process_raw_to_tokens(content)
        print "Process raw to tokens: " + str(time.time() - start_time) + " seconds"
        # print "processed terms", terms

        gramDict = self.dict

        tflist = []
        position = 0 # 0-based index for position
        start_time = time.time()
        for term in terms:
            # print position, term
            rawtf = terms.count(term)
            weightedtf = Indexer.logFreq(rawtf)
            tflist.append(weightedtf)

            if term not in gramDict:
                # first time seeing term
                gramDict[term] = {}
                gramDict[term]['pos'] = None # seek pointers
                gramDict[term]['len'] = 0 # bytes to read
                gramDict[term]['p'] = Posting(docId, weightedtf)
                gramDict[term]['p'].addPos(docId, position)
                gramDict[term]['df'] = 1

            else :
                # appeared in other docs
                posting = gramDict[term]['p']
                posting.add(docId, weightedtf)
                posting.addPos(docId, position)
                gramDict[term]['df'] += 1

            position += 1
        print "Added terms to gramDict: " + str(time.time()-start_time) + " seconds"

        # calculate cosine length for each gram
        start_time = time.time()
        cosLength = Indexer.calculateVectorLength(tflist)
        print "Calculate vector length: " + str(time.time()-start_time) + " seconds"
        start_time = time.time()
        self.normalise(docId, terms, cosLength)
        print "Normalise: " + str(time.time()-start_time) + " seconds"


        self.numDocs += 1

    def normalise(self, docId, setTerms, cosLength):
        gramDict = self.dict
        for term in setTerms:
            posting = gramDict[term]['p']
            weightedtf = gramDict[term]['p'].getTf(docId)
            posting.updateTf(docId, weightedtf/cosLength)

    def process(self, content):
        """
        Given raw text content, we perform the following operations:
        casefolding, tokenizing, stemming, stripping punctuation
        """
        # print "processing:",
        # print content
        tokens = []
        sentences = nltk.sent_tokenize(content)
        for sentence in sentences:
            words = self.tokenizer.tokenize(sentence.lower())
            processed = []
            for word in words:
                try:
                    stemmed_word = self.stemmer.stem(word)
                    processed.append(stemmed_word)
                except:
                    processed.append(word)
            # processed = [self.stemmer.stem(word) for word in words if len(word) >= 2]
            tokens.extend(processed)
        return tokens

    def save(self):
        self.writeToPostingFile()
        self.writeToDictFile()

    def writeToDictFile(self):
        start_time = time.time()
        with open(self.dictionary_fname, 'wb+') as f:
            f.write(json.dumps(self.dict))
        print "Write to dict file: " + str(time.time()-start_time) + " seconds"

    def writeToPostingFile(self):
        start_time = time.time()
        """
        Dump using cpickle
        keep track of size and pos
        delete the posting list now so it won't be written to the dictionary file later on
        """
        with open(self.posting_fname, 'wb+') as f:
            gramDict = self.dict
            # print "gramDict", gramDict

            # for k in gramDict.keys():
            #     print "key", k
            #     print "value", gramDict[k]
            #     posting = gramDict[k]['p']
            #     print "posting", posting
            #     for j in posting.getKeys():
            #         print "posting key", j
            #         print "posting dict", posting.getTf(j)
            #         print "posting pos", posting.getPos(j)


            for k, v in gramDict.iteritems():
                startPos = f.tell()
                cPickle.dump(v['p'], f)
                del v['p']
                endPos = f.tell()
                v['pos'] = startPos

        print "Write to posting file: " + str(time.time() - start_time) + " seconds"
    # def dump(self):
    #     gramDict = self.dict
    #     for k, v in gramDict.iteritems():
            # print k,v
            # print k,
            # print(json.dumps(v['p'].dict))
            # del v['p']
            # print k, v

    @staticmethod
    def logFreq(tf):
        if tf < 0:
            return 0
        return 1 + math.log10(tf)

    @staticmethod
    def calculateVectorLength(tflist):
        # Given a list, it squares the elems, sum and root
        temp = list(map(lambda x: x**2, tflist))
        res = sum(temp)
        return math.sqrt(res)

def main(document_dname, dictionary_fname, posting_fname):

    indexer = Indexer(dictionary_fname, posting_fname)
    regexCleaner = Cleaner()
    corpora = os.listdir(document_dname)

    # sort in ascending numeric order
    for file in sorted(corpora, key=numericalSort):
        if file[0] is ".":
            continue
        else:
            print file
            file_obj = open(document_dname + file, "r")
            content = regexCleaner.clean(file_obj)
            docId = re.findall(r"\d+", file)[0]
            # print "Regex"
            # print re.findall(r"\d+", file)
            docObj = {}
            docObj['content'] = content
            docObj['docId'] = docId
            indexer.addDoc(docObj)

    indexer.save()

    # After cleaning out css, return one object per document
    # for file in directory:
    #     data = readfile(file)
    #     docObj = clean(data)
    #     indexer.addDoc(doc)
    # indexer.save()

    # stub objects
    # docObj = {'docId': '555', \
    #           'content': 'the quick brown fox [2008] jumps over the lazy (i) dog. the lazy fox quickly says hello.'}
    # docObj2 = {'docId': '879', \
    #           'content': 'the lovely fox [2008] (i) do not say hello to the lazy dog.'}
    # docs = [docObj, docObj2]
    #
    # for doc in docs:
    #     indexer.addDoc(doc)


def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1:2] = map(int, parts[1:2])
    return parts


def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"


input_file_i = input_file_d = input_file_p = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        input_file_i = a
    elif o == '-d':
        input_file_d = a
    elif o == '-p':
        input_file_p = a
    else:
        assert False, "unhandled option"
if input_file_i is None or input_file_d is None or input_file_p is None:
    usage()
    sys.exit(2)

start_time = time.time()
main(input_file_i, input_file_d, input_file_p)
print "Total time: %s seconds" % (time.time() - start_time)
