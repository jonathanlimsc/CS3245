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
def get_doc_freq(term, vector, dictionary, terms_in_all_or_none):
    doc_freq = 1 # to avoid divide by zero before removal
    if dictionary.has_term(term):
        doc_freq = dictionary.doc_freq_hash[term]
    else:
        terms_in_all_or_none.append(term)
        print term, "not in dictionary so will be removed from query vector"
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
    terms_in_all_or_none = []
    print "raw tf for query", vector
    squares_sum = 0
    for term in vector:
        print "Term:", term
        vector[term] = math.log(vector[term], 10) + 1
        print "after first log:", vector[term]
        doc_freq = get_doc_freq(term, vector, dictionary, terms_in_all_or_none)
        total_docs = len(dictionary.doc_ids)

        print "total_docs =", total_docs, "doc_freq =", doc_freq
        if total_docs != doc_freq:
            vector[term] *= math.log(total_docs/doc_freq, 10)
            squares_sum += vector[term]
            print "after second log:", vector[term]
        else:
            terms_in_all_or_none.append(term)
            print term, "present in all docs so will be removed query vector"


    for term in terms_in_all_or_none:
        vector.pop(term)
        print "removed", term, "from query vector"
    square_root_of_squares = math.pow(squares_sum, 1/2)
    for term in vector:
        vector[term] /= square_root_of_squares

    print "W(t,q) for query", vector
    return vector

def add_term_to_score(document_scores, document_squares, doc_id, term_freq, query_weight):
    term_weight = math.log(term_freq, 10) + 1
    if doc_id in document_scores:
        document_scores[doc_id] += term_weight * query_weight
        document_squares[doc_id] += math.pow(term_weight, 2)
    else:
        document_scores[doc_id] = term_weight * query_weight
        document_squares[doc_id] = math.pow(term_weight, 2)

def add_terms_to_scores(document_scores, document_squares, term, query_weight,
        dictionary, postings_file):
    if term not in dictionary.start_ptr_hash:
        print "WARN:", term, "not in dictinoary.start_ptr_hash!"
        print "Exiting..."
        sys.exit(2)
    start_ptr = dictionary.start_ptr_hash[term]
    p_entry = postings_file.read_posting_entry(start_ptr)
    add_term_to_score(document_scores, document_squares, p_entry.doc_id, p_entry.term_freq, query_weight)
    while p_entry.next_ptr != -1:
        print "p_entry.next_ptr", p_entry.next_ptr
        p_entry = postings_file.read_posting_entry(p_entry.next_ptr)
        add_term_to_score(document_scores, document_squares, p_entry.doc_id, p_entry.term_freq, query_weight)

def normalize_scores(document_scores, document_squares, query_vector):
    for doc_id in document_squares:
        document_squares[doc_id] = math.pow(document_squares[doc_id], 1/2)
    for doc_id in document_scores:
        document_scores[doc_id] /= document_squares[doc_id]

def get_top_ten_docs(document_scores):
    #TODO further sort when relevance score is equal
    heap = [(-score, doc_id) for doc_id,score in document_scores.items()]
    print "heap", heap
    top_ten = heapq.nsmallest(10, heap)
    print "top_ten", top_ten
    doc_ids = []
    for score in top_ten:
        print "score", score, score[1]
        doc_ids.append(score[1])

    print "doc_ids", doc_ids
    return doc_ids

def process_query(query, dictionary, postings_file):
    result = []
    with PostingFile(postings_file, 'r') as postings_file:
        query_terms = get_normal_terms(query)
        query_vector = create_query_vector(query_terms, dictionary, postings_file)
        if len(query_vector) == 0:
            print "NOTE: each term in", query_terms, "is either absent from dictionary or present in every doc"
            return result

        document_scores = {}
        document_squares = {}

        for term in query_vector.keys():
            add_terms_to_scores(document_scores, document_squares, term, query_vector[term], dictionary, postings_file)
        print "document_scores:", "\n\t", document_scores
        print "document_squares:", "\n\t", document_squares

        normalize_scores(document_scores, document_squares, query_vector)
        result = get_top_ten_docs(document_scores)

    postings_file.close()

    return result

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
