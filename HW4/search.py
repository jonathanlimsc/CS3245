import getopt
import sys
import json
import cPickle
from posting import *
from utils import process_raw_to_tokens
from sets import Set
from nltk.corpus import wordnet

def process_query(query):
    """
    Process a query string. Splits a query string into constituent phrases
    separated by AND, and generates the tokens from each phrase
    """
    phrases_arr = []
    phrases = query.split('AND')
    print phrases
    for phrase in phrases:
        terms = process_raw_to_tokens(phrase)
        print "Terms: " + str(terms)
        phrases_arr.append(terms)
        print "Tokenized phrase array: " + str(phrases_arr)
    return phrases_arr

def merge_list_without_position(list_1, list_2):
    """
    A simple AND merge of two lists of doc IDs.
    Positional indices are not considered.
    This function is called for non-final (not last) terms in a phrase.
    """
    result = []
    idx_1 = 0
    idx_2 = 0
    while idx_1 < len(list_1) and idx_2 < len(list_2):
        if list_1[idx_1] < list_2[idx_2]:
            idx_1 += 1
        elif list_1[idx_1] > list_2[idx_2]:
            idx_2 += 1
        else:
            # Common doc_id found
            doc_id = list_1[idx_1]
            result.append(doc_id)
            idx_1 += 1
            idx_2 += 1
    print "Merged ids without position " + str(result)
    return result

def merge_list_with_position(list_1, list_2, prev_postings, curr_posting):
    """
    Merges two lists of doc IDs, taking into account position indices
    prev_postings : an array of posting lists of the previous terms
    curr_posting: the posting list of the current term

    This function is called for the final term in the phrase.
    """
    result = []
    idx_1 = 0
    idx_2 = 0
    while idx_1 < len(list_1) and idx_2 < len(list_2):
        if list_1[idx_1] < list_2[idx_2]:
            idx_1 += 1
        elif list_1[idx_1] > list_2[idx_2]:
            idx_2 += 1
        else:
            # There is a doc_id match, but we need to check positions to fulfil the phrase
            doc_id = list_1[idx_1]
            pos_idx = 0
            offset = len(prev_postings)
            curr_pos = curr_posting.getPos(doc_id)

            # For each position number in current posting list
            for pos in curr_pos:
                # Find match with offset in prev_postings. Matches must == len(prev_postings) to fulfil phrasal query
                match = 0
                while pos_idx < len(prev_postings):
                    prev_posting = prev_postings[pos_idx]
                    prev_pos = prev_posting.getPos(doc_id)
                    # If there is a term at position (pos-offset) in prev_posting, it fulfils a part of the phrase
                    if (pos - offset) in prev_pos:
                        match += 1
                        pos_idx += 1
                        offset -= 1
                    else:
                        # If even one check fails, move on to check the next position
                        break

                # Found a doc_id which fulfils phrasal query, stop finding positions
                if match == len(prev_postings):
                    result.append(doc_id)
                    break

            # Increment idx_1 and idx_2, move on to the next doc_id
            idx_1 += 1
            idx_2 += 1

    print "Merged ids with position: " + str(result)
    return result


def get_doc_ids_for_phrase(phrase_tokens, dictionary, posting_file):
    """
    Returns a list of doc_ids as result of the search for a given list of phrase tokens.
    """
    if len(phrase_tokens) == 1:
        token = phrase_tokens[0]
        posting = get_posting(dictionary, posting_file, token)
        if posting is not None:
            doc_ids = posting.getDocIds()
            return doc_ids
        else:
            return []

    merged_ids = []
    prev_postings = []
    for idx in range(len(phrase_tokens)):
        token = phrase_tokens[idx]
        print "token: " + token
        posting = get_posting(dictionary, posting_file, token)
        if posting is None:
            return []
        # For first token
        if idx == 0:
            merged_ids.extend(posting.getDocIds())
            print "First pass: " + str(merged_ids)
            print ""
            prev_postings.append(posting)
        # Subsequent tokens but not the last token
        elif idx < len(phrase_tokens) - 1:
            curr_ids = posting.getDocIds()
            merged_ids = merge_list_without_position(merged_ids, curr_ids)
            prev_postings.append(posting)
            print "Intermediate pass: " + str(merged_ids)
            print ""
        else:
            curr_ids = posting.getDocIds()
            merged_ids = merge_list_with_position(merged_ids, curr_ids, prev_postings, posting)
            print "Final pass: " + str(merged_ids)
            print ""

    return merged_ids

def main(dictionary_fname, posting_fname, query_fname, output_fname):
    # For each query phrase
    # Split terms 1, 2, 3 (max is 3)
    #  Postings list of t1 merge (AND) with t2
    #  For each match in a docID, check if position matches
    # Result postings list merge with t3
        # Retrieve docsIds for term 1
        # Retrieve docIds for term 2
    with open(dictionary_fname, 'r') as dictionary_file:
        with open(posting_fname, 'r') as posting_file:
            with open(query_fname, 'r') as query_file:
                with open(output_fname, 'w') as output_file:
                    dictionary = json.load(dictionary_file)
                    for query in query_file:
                        print "---------- QUERY: " + query
                        phrases = process_query(query)
                        doc_ids = Set([])
                        for idx in range(len(phrases)):
                            phrase_tokens = phrases[idx]
                            if idx == 0:
                                result = get_doc_ids_for_phrase(phrase_tokens, dictionary, posting_file)
                                doc_ids = doc_ids.union(result)
                            else:
                                doc_ids = doc_ids.intersection(get_doc_ids_for_phrase(phrase_tokens, dictionary, posting_file))

                        sorted_result = sorted(doc_ids, key=int)
                        output_str = ' '.join(sorted_result)
                        output_file.write(output_str + "\n")
                        print "Output string: " + output_str
                        print "Result of search (unsorted): " + str(doc_ids)
                        print "Result of search (sorted): " + str(sorted_result)
                        print ""

                output_file.close()
            query_file.close()
        posting_file.close()
    dictionary_file.close()

def get_posting(dictionary, posting_file, term):
    if term not in dictionary:
        print "Note:", term, "does not appear in dictionary"
        return None
    dictionary_entry = dictionary[term]
    pos = dictionary_entry['pos']
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
