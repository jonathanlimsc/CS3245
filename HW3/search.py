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
sort = True
count = 0
def search(dict_file, postings_file, queries_file, results_file):
    global count
    dictionary = Dictionary.load_dict_from_file(dict_file)
    print len(dictionary.doc_ids)
    with open(queries_file, 'r') as query_f:
        with open(results_file, 'w') as results_f:
            for query in query_f:
                result = process_query(query, dictionary, postings_file)
                result = [str(x) for x in result]
                result_str = " ".join(result) + "\n"
                results_f.write(result_str)
                count += 1
                if count == 2:
                    sys.exit(2)
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
    total_docs = len(dictionary.doc_ids)
    for term in vector:
        print "Term:", term
        vector[term] = 1.0 * math.log(vector[term], 10) + 1.0
        print "after first log:", vector[term]
        doc_freq = get_doc_freq(term, vector, dictionary, terms_in_all_or_none)

        # print "total_docs =", total_docs, "doc_freq =", doc_freq
        if total_docs != doc_freq:
            vector[term] *= math.log(1.0 * total_docs/doc_freq, 10)
            print "Vector term: ", vector[term]
            squares_sum += math.pow(vector[term], 2)
            print "after second log:", vector[term]
        else:
            # For case where term appears in all docs. Currently we remove them from query
            # TODO: KIV, what if the query is only made up of terms that are present in all docs
            terms_in_all_or_none.append(term)
            print term, "present in all docs so will be removed from query vector"


    for term in terms_in_all_or_none:
        vector.pop(term)
        print "removed", term, "from query vector"

    square_root_of_squares = math.sqrt(squares_sum)

    print "Squares sum: ", squares_sum
    for term in vector:
        vector[term] /= square_root_of_squares

    print "W(t,q) for query", vector
    return vector

def add_term_to_score(document_scores, document_squares, doc_id, term_freq, query_weight):
    term_weight = 1.0 * math.log(term_freq, 10) + 1.0
    if doc_id in document_scores:
        document_scores[doc_id] += term_weight * query_weight
        document_squares[doc_id] += math.pow(term_weight, 2)
    else:
        document_scores[doc_id] = 1.0 * term_weight * query_weight
        document_squares[doc_id] = 1.0 * math.pow(term_weight, 2)

def add_terms_to_scores(document_scores, document_squares, term, query_weight,
        dictionary, postings_file):
    start_ptr = dictionary.start_ptr_hash[term]
    p_entry = postings_file.read_posting_entry(start_ptr)
    while p_entry != None:
        add_term_to_score(document_scores, document_squares, p_entry.doc_id, p_entry.term_freq, query_weight)
        p_entry = postings_file.get_next_entry(p_entry)

def normalize_scores(document_scores, document_squares, query_vector):
    for doc_id in document_squares:
        document_squares[doc_id] = math.sqrt(document_squares[doc_id])
    for doc_id in document_scores:
        document_scores[doc_id] /= 1.0 * document_squares[doc_id]
    print "normalized document_scores", document_scores

def get_top_ten_docs(document_scores):
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
        if sort:
            result.sort()

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
