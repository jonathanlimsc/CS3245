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
def get_doc_freq(term, vector, dictionary):
    doc_freq = 0
    if dictionary.has_term(term):
        doc_freq = dictionary.doc_freq_hash[term]
    else:
        vector.pop(term)
        print term, "not in dictionary so removing it from query vector"
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
    terms_in_all_docs = []
    print "raw tf for query", vector

    for term in vector:
        # print "Term:", term
        vector[term] = math.log(vector[term], 10) + 1
        # print "after first log:", vector[term]
        doc_freq = get_doc_freq(term, vector, dictionary)
        total_docs = len(dictionary.doc_ids)

        # print "total_docs =", total_docs, "doc_freq =", doc_freq
        if total_docs != doc_freq:
            vector[term] *= math.log(total_docs/doc_freq, 10)
            # print "after second log:", vector[term]
        else:
            terms_in_all_docs.append(term)

    for term in terms_in_all_docs:
        vector.pop(term)
        # print term, "is present in all docs so removing it from query vector"

    print "W(t,q) for query", vector
    return vector

def add_term_to_score(document_scores, doc_id, term_freq, query_weight):
    if doc_id in document_scores:
        document_scores[doc_id] += (math.log(term_freq, 10) + 1) * query_weight
    else:
        document_scores[doc_id] = (math.log(term_freq, 10) + 1) * query_weight

def add_terms_to_scores(document_scores, term, query_weight,
        dictionary, postings_file):
    start_ptr = dictionary.start_ptr_hash[term]
    p_entry = postings_file.read_posting_entry(start_ptr)
    add_term_to_score(document_scores, p_entry.doc_id, p_entry.term_freq, query_weight)
    while p_entry.next_ptr != -1:
        p_entry = postings_file.read_posting_entry(p_entry.next_ptr)
        add_term_to_score(document_scores, p_entry.doc_id, p_entry.term_freq, query_weight)


def process_query(query, dictionary, postings_file):
    with PostingFile(postings_file, 'r') as postings_file:
        heap = []
        query_terms = get_normal_terms(query)
        query_vector = create_query_vector(query_terms, dictionary, postings_file)
        document_scores = {}

        for term in query_vector.keys():
            add_terms_to_scores(document_scores, term, query_vector[term], dictionary, postings_file)
        print "document_scores:"
        print "\t", document_scores

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
