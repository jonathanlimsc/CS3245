import getopt
import sys
import json
import cPickle
from posting import *

def main(dictionary_fname, posting_fname, query_fname, output_fname):
    # Example reading files
    with open(dictionary_fname) as dictionary_file:
        with open(posting_fname) as posting_file:
            dictionary = json.load(dictionary_file)
            term = 'the'
            posting = get_posting(dictionary, posting_file, term)

            if posting is not None:
                for docId in posting.getKeys():
                    print "docId", docId
                    print "\t", posting.getTf(docId) # returns tf
                    print "\t", posting.getPos(docId) # returns list of positions





            posting_file.close()
        dictionary_file.close()

def get_posting(dictionary, posting_file, term):
    if term not in dictionary:
        print "Note:", term, "does not appear in dictionary"
        return None
    dictionary_entry = dictionary[term]
    pos = dictionary_entry['pos']
    length = dictionary_entry['len'] # unused
    posting_file.seek(pos,0)
    posting = cPickle.load(posting_file)
    return posting


def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"


input_file_d = input_file_p = input_file_q = output_file_o = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        input_file_d = a
    elif o == '-p':
        input_file_p = a
    elif o == '-q':
        input_file_q = a
    elif o == '-o':
        output_file_o = a
    else:
        assert False, "unhandled option"
if input_file_d == None or input_file_p == None or input_file_q == None or output_file_o == None:
    usage()
    sys.exit(2)

main(input_file_d, input_file_p, input_file_q, output_file_o)
