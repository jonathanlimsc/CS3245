import getopt
import sys
from dictionary import Dictionary
from postingfile import PostingFile
import query_parser
import boolops
from utils import normalize_token
from nltk.tokenize import word_tokenize
from math import log
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

# for every term, docID pair,
# tf_list maps docIDs to their tf
def compute_term_frequency(term, dict, postings_file, tf_list):
    p_list = []
    if dict.has_term(term):
        start_ptr = dict.start_ptr_hash[term]
        p_list = postings_file.read_posting_entry(start_ptr)
        print "read_posting_entry", p_list.doc_id, p_list.term_freq, p_list.next_ptr
        while p_list.next_ptr != -1:
            p_list = postings_file.read_posting_entry(p_list.next_ptr)
            print "\t", p_list.doc_id, p_list.term_freq, p_list.next_ptr
    else:
        print term, "not in dict"
    return []

# def compute_tf_idf(term, dict, postings_file):
#     tf = compute_tf(term, dict)

# count occurences of each term in query and assign raw tf weight
def get_tf_raw_for_query(terms):
    vector = {}
    for term in terms:
        if term not in vector:
            vector[term] = 1
        else:
            vector[term] = vector[term] + 1
    print "get_tf_raw_for_query", vector
    return vector

def create_query_vector(terms, dict, postings_file):
    vector = get_tf_raw_for_query(terms)
    # for term in terms:
    #     tf_idf = compute_tf_idf(term, dict, postings_file)
    #     print "tf_idf =", tf_idf
    #     vector[term] = tf_idf
    print vector


def process_query(query, dict, postings_file):
    with PostingFile(postings_file, 'r') as postings_file:
        heap = []
        terms = get_normal_terms(query)
        query_vector = create_query_vector(terms, dict, postings_file)
        print query.strip(), "->", terms
        tf_list = []
        for term in terms:
            tf_list = compute_term_frequency(term, dict, postings_file, tf_list)

    postings_file.close()

    return []#result

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
