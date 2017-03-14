import getopt
import sys
from dictionary import Dictionary
from postingfile import PostingFile
import query_parser
import boolops
from utils import normalize_token
from nltk.tokenize import word_tokenize

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

def get_normal_tokens(query):
    query = query.strip()
    query = normalize_token(query)
    tokens = word_tokenize(query)
    normal_tokens = []
    for token in tokens:
        token = normalize_token(token)
        token = token.encode('ascii') #removes 'u' from print
        normal_tokens.append(token)
    return normal_tokens

def get_posting_list(term, dict, postings_file):
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

def process_query(query, dict, postings_file):
    with PostingFile(postings_file, 'r') as postings_file:
        tokens = get_normal_tokens(query)
        print query, "->", tokens
        for term in tokens:
            p_list = get_posting_list(term, dict, postings_file)


        ''' TODO: tokenize queries, create query vector. Per query term,
            1. Get posting list
            2. Calculate W(t,d) = log(term_freq in doc)+1 for each posting entry
            3. Calculate W(t,q) = (log(term_freq in query)+1) * (log(N/doc_freq)) for the query term
            4. Multiply 2. and 3., increment score[doc_id]
            5. Increment square[doc_id] by W(t,d)^2 (for calculating length of document vector later to normalize)

            Divide each score[doc_id] with sqrt(square[doc_id]) and length of query vector
            Result is cos(querytermvector, documentvector)

            Sort the score array and return top 10 (1 is similar, 0 is dissimilar)

        '''
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
