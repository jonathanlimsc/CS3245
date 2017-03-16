import getopt
import sys
from dictionary import Dictionary
from postingfile import PostingFile
import query_parser
import boolops
from utils import normalize_token
from nltk.tokenize import word_tokenize
import math
import heapq

def search(dict_file, postings_file, queries_file, results_file):
    dictionary = Dictionary.load_dict_from_file(dict_file)
    print dictionary.doc_freq_hash.keys()
    print len(dictionary.doc_ids)
    with open(queries_file, 'r') as query_f:
        with open(results_file, 'w') as results_f:
            for query in query_f:
                result = process_query(query, dictionary, postings_file)
                result = [str(x) for x in result]
                result_str = " ".join(result) + "\n"
                results_f.write(result_str)
        results_f.close()
    query_f.close()

def get_normal_terms(query):
    query = query.strip()
    terms = word_tokenize(query)
    normal_terms = []
    for term in terms:
        term = normalize_token(term)
        term = term.encode('ascii') #removes 'u' from print
        normal_terms.append(term)
    return normal_terms

# if present, returns the document frequency for a term in the dictionary, 1 otherwise
def get_doc_freq(term, dictionary):
    doc_freq = 0
    if dictionary.has_term(term):
        doc_freq = dictionary.doc_freq_hash[term]
    else:
        doc_freq = 1
        print term, "not in dictionary, how to compute?"
    print "doc_freq =", doc_freq
    return doc_freq

def get_term_frequency_in_query(terms):
    vector = {}
    for term in terms:
        if term not in vector:
            vector[term] = 1
        else:
            vector[term] = vector[term] + 1
    return vector

def create_query_vector(query_terms, dictionary, postings_file):

    vector = get_term_frequency_in_query(query_terms)

    print "raw tf for query", vector

    for term in vector:
        vector[term] = math.log(vector[term], 10) + 1
        print "after first log:", vector[term]
        doc_freq = get_doc_freq(term, dictionary)
        total_docs = len(dictionary.doc_ids)

        print "total_docs =", total_docs
        vector[term] *= math.log(total_docs/doc_freq, 10)
        print "after second log:", vector[term]

    print "W(t,q) for query", vector
    return vector

# for every term, docID pair,
# tf_list maps docIDs to their tf
def create_document_vector(term, dictionary, postings_file,
        document_vectors, query_vector):

    query_terms = query_vector.keys()
    document_vector = {}

    if dictionary.has_term(term) and term in query_terms:
        start_ptr = dictionary.start_ptr_hash[term]
        p_entry = postings_file.read_posting_entry(start_ptr)

        document_vector[p_entry.doc_id] = log(p_entry.term_freq, 10) + 1
        while p_entry.next_ptr != -1:
            p_entry = postings_file.read_posting_entry(p_entry.next_ptr)
            document_vector[p_entry.doc_id] = log(p_entry.term_freq, 10) + 1
    else:
        print term, "not in dictionary, so what?"
    return document_vector

def process_query(query, dictionary, postings_file):
    with PostingFile(postings_file, 'r') as postings_file:
        heap = []
        query_terms = get_normal_terms(query)
        query_vector = create_query_vector(query_terms, dictionary, postings_file)
        document_vectors = []

        for term in query_terms:
            document_vectors[term] = create_document_vector(term, dictionary, postings_file, document_vectors, query_vector)

    postings_file.close()

    return heap

def usage():
    print "Usage: " + sys.argv[0] + " -d <dictionary-file> -p <postings-file> -q <queries-file> -o <results-file>"


dict_file = postings_file = queries_file = results_file = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        dict_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        queries_file = a
    elif o == '-o':
        results_file = a
    else:
        assert False, "unhandled option"

if dict_file == None or postings_file == None or queries_file == None or results_file == None:
    usage()
    sys.exit(2)

search(dict_file, postings_file, queries_file, results_file)
