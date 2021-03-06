import getopt
import sys
import os
from os.path import isfile, join, basename
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from dictionary import Dictionary
from postingfile import PostingFile
from utils import normalize_token, calculate_tf_wt
import cPickle
import math
from collections import Counter

def build_index(dir_of_docs, dict_file, postings_file):
    docs = [f for f in os.listdir(dir_of_docs) if isfile(join(dir_of_docs, f)) and f.isdigit()]
    # print docs
    sorted_doc_ids = sorted(docs, key=lambda x: int(basename(x)))
    # print sorted_doc_ids
    dictionary = Dictionary()
    with PostingFile(postings_file, 'w+') as p_file:
        for doc_id in sorted_doc_ids:
            doc_path = dir_of_docs + '/' + doc_id
            terms = process_file(doc_path)
            counter = Counter(terms)
            print "Indexing document ", str(doc_id) + "..."
            # print counter
            # print "There are " + str(len(terms)) + " terms"
            document_vector = {}
            for term, freq in counter.iteritems():

                p_file.file_obj.seek(0, os.SEEK_END)
                curr_ptr = p_file.file_obj.tell()

                doc_id = int(doc_id)

                if dictionary.has_term(term):
                    # Overwrite previous posting entry for the term
                    prev_entry_ptr = dictionary.end_ptr_hash[term]
                    prev_entry = p_file.read_posting_entry(prev_entry_ptr)
                    p_file.write_posting_entry(prev_entry.doc_id, prev_entry.term_freq, curr_ptr, overwrite_pos=prev_entry_ptr)

                # Write new entry to posting file at end
                p_file.write_posting_entry(doc_id, freq)

                dictionary.add_term(term, doc_id, curr_ptr)

                # Build document_vector
                document_vector[term] = calculate_tf_wt(freq)

            # print "Document vector: ", document_vector
            # Save document length into dictionary
            document_length = calculate_document_length(document_vector)
            # print "Document length: ", document_length
            dictionary.doc_id_length_hash[doc_id] = document_length

        # print "dictionary doc ids to length: ", dictionary.doc_id_length_hash
        # Check if the dictionary and postings are ok
        # print_term_to_postings(dictionary, p_file)

    p_file.close()

    # Save dictionary to file
    dictionary.save_dict_to_file(dict_file)

def calculate_document_length(document_vector):
    document_length = 0
    for term, wt in document_vector.iteritems():
        document_length += math.pow(wt, 2)
    document_length = math.pow(document_length, 0.5)

    return document_length

def print_term_to_postings(dictionary, p_file):
    # Read postings list to test for correctness
    # print str(len(dictionary.doc_freq_hash.keys())) + " terms in dictionary"
    for term in dictionary.doc_freq_hash.keys():
        start_ptr = dictionary.start_ptr_hash[term]
        # print "term: " + term + " "
        doc_ids = []
        pe = p_file.read_posting_entry(start_ptr)
        while pe is not None:
            doc_ids.append(pe.doc_id)
            pe = p_file.get_next_entry(pe)
        # print doc_ids
        # print dictionary.doc_freq_hash[term]

def process_file(doc_path):
    with open(doc_path, 'r') as doc:
        terms = []
        for line in doc:
            tokens = tokenize(line)
            for term in normalize_tokens(tokens):
                terms.append(term)
        # print terms
        # print " "
    doc.close()
    return terms

def tokenize(doc_string):
    tokens = []
    for sentence in sent_tokenize(doc_string):
        tokens.extend(word_tokenize(sentence))
    return tokens

def normalize_tokens(tokens):
    '''
    Case folding and stemming
    '''
    result = [normalize_token(token) for token in tokens if len(token) > 0]

    return result

def usage():
    print "Usage: " + sys.argv[0] + " -i <directory-of-docs> -d <dictionary-file> -p <postings-file>"


dir_of_docs = dict_file = postings_file = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        dir_of_docs = a
    elif o == '-d':
        dict_file = a
    elif o == '-p':
        postings_file = a
    else:
        assert False, "unhandled option"

if dir_of_docs == None or dict_file == None or postings_file == None:
    usage()
    sys.exit(2)

build_index(dir_of_docs, dict_file, postings_file)
