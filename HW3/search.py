import getopt
import sys
from dictionary import Dictionary
from postingfile import PostingFile
import query_parser
import boolops

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

def process_query(query, dict, postings_file):
    with PostingFile(postings_file, 'r') as postings_file:
        query_tokens = query_parser.convert_query_to_bool_exp(query)
        query_post_fix = query_parser.convert_to_postfix(query_tokens)
        result = execute_bool_query(query_post_fix, dict, postings_file)
    postings_file.close()

    return result

def execute_bool_query(query, dict, postings_f):
    '''
    Boolean query is given in post-fix notation. Executes it
    and returns doc ids.
    '''
    operators = query_parser.operators

    idx = 0
    query_len = len(query)
    operand_stack = []
    for token in query:
        if token in operators:
            if len(operand_stack) > 0:
                if token == 'NOT':
                    term = operand_stack.pop()
                    result = not_op(term, dict, postings_f)
                elif token == 'AND':
                    term1 = operand_stack.pop()
                    term2 = operand_stack.pop()
                    result = and_op(term1, term2, dict, postings_f)
                elif token == 'OR':
                    term1 = operand_stack.pop()
                    term2 = operand_stack.pop()
                    result = or_op(term1, term2, dict, postings_f)
                # Add result back to operand_stack
                operand_stack.append(result)
        else:
            # Normal tokens
            operand_stack.append(token)

    # Final result
    result = operand_stack.pop()
    print result
    return result

def not_op(term, dict, postings_f):
    '''
    Checks whether term1 and term2 are terms or intermediate results.
    Executes the appropriate function.
    '''
    if isinstance(term, basestring):
        if dict.has_term(term):
            start_ptr = dict.start_ptr_hash[term]
            p = postings_f.read_posting_entry(start_ptr)
            return boolops.plist_not(p, dict.doc_ids, postings_f)
        else:
            return list(dict.doc_ids)
    else:
        # Undefined. NOT should not be applied on intermediate results.
        return []

def and_op(term1, term2, dict, postings_f):
    '''
    Checks whether term1 and term2 are terms or intermediate results.
    Executes the appropriate function.
    '''
    if isinstance(term1, basestring) and isinstance(term2, basestring):
        if dict.has_term(term1) and dict.has_term(term2):
            start_ptr1 = dict.start_ptr_hash[term1]
            p1 = postings_f.read_posting_entry(start_ptr1)
            start_ptr2 = dict.start_ptr_hash[term2]
            p2 = postings_f.read_posting_entry(start_ptr2)
            return boolops.plist_and(p1, p2, postings_f)
        else:
            return []
    elif isinstance(term1, basestring) and not isinstance(term2, basestring):
        if dict.has_term(term1):
            start_ptr = dict.start_ptr_hash[term1]
            p = postings_f.read_posting_entry(start_ptr)
            return boolops.plist_list_and(p, term2, postings_f)
        else:
            return []
    elif not isinstance(term1, basestring) and isinstance(term2, basestring):
        if dict.has_term(term2):
            start_ptr = dict.start_ptr_hash[term2]
            p = postings_f.read_posting_entry(start_ptr)
            return boolops.plist_list_and(p, term1, postings_f)
        else:
            return []
    else:
        # Both are intermediate results
        return boolops.list_and(term1, term2)

def or_op(term1, term2, dict, postings_f):
    '''
    Checks whether term1 and term2 are terms or intermediate results.
    Executes the appropriate function.
    '''
    if isinstance(term1, basestring) and isinstance(term2, basestring):
        if dict.has_term(term1) and dict.has_term(term2):
            start_ptr1 = dict.start_ptr_hash[term1]
            start_ptr2 = dict.start_ptr_hash[term2]
            p1 = postings_f.read_posting_entry(start_ptr1)
            p2 = postings_f.read_posting_entry(start_ptr2)
            return boolops.plist_or(p1, p2, postings_f)
        elif dict.has_term(term1) and not dict.has_term(term2):
            start_ptr = dict.start_ptr_hash[term1]
            p = postings_f.read_posting_entry(start_ptr)
            return boolops.plist_list_or(p1, [], postings_f)
        elif not dict.has_term(term1) and dict.has_term(term2):
            start_ptr = dict.start_ptr_hash[term2]
            p = postings_f.read_posting_entry(start_ptr)
            return boolops.plist_list_or([], p, postings_f)
        else:
            return []
    elif isinstance(term1, basestring) and not isinstance(term2, basestring):
        if dict.has_term(term1):
            start_ptr = dict.start_ptr_hash[term1]
            p = postings_f.read_posting_entry(start_ptr)
            return boolops.plist_list_or(p, term2, postings_f)
        else:
            return term2
    elif not isinstance(term1, basestring) and isinstance(term2, basestring):
        if dict.has_term(term2):
            start_ptr = dict.start_ptr_hash[term2]
            p = postings_f.read_posting_entry(start_ptr)
            return boolops.plist_list_or(p, term1, postings_f)
        else:
            return term1
    else:
        # Both are intermediate results
        return boolops.list_or(term1, term2)


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
