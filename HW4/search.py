import getopt
import sys
import json
import cPickle
from posting import *
from utils import process_raw_to_tokens

def process_query(query):
    phrases_arr = []
    print query
    phrases = query.split('AND')
    print phrases
    for phrase in phrases:
        terms = process_raw_to_tokens(phrase)
        print terms
        phrases_arr.append(terms)
        print phrases_arr
    return phrases_arr

def merge_posting_list(list_1, list_2, prev_postings):
    result = []
    idx_1 = 0
    idx_2 = 0
    while idx_1 != len(list_1) and idx_2 != len(list_2):
        if list_1[idx_1] < list_2[idx_2]:
            idx_1 += 1
        else if list_1[idx_1] > list_2[idx_2]:
            idx_2 += 1
        else:
            # There is a doc_id match, but we need to check positions to fulfil the phrase
            doc_id = list_1[idx_1]
            pos_idx = 0
            offset = len(prev_postings)
            curr_pos = posting.getPos(doc_id)

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

    print result
    return result


def get_doc_ids_for_phrase(tokens, dictionary, posting_file):
    if len(phrase_tokens) == 1:
        posting = get_posting(dictionary, posting_file, token)
        if posting is not None:
            doc_ids = posting.getKeys()
            return doc_ids
        else:
            return []

    doc_ids = []
    merged_ids = []
    prev_postings = []
    for idx in range(len(phrase_tokens)):
        token = phrase_tokens[idx]
        posting = get_posting(dictionary, posting_file, token)
        # Only 1 token
        if idx == 0:
            merged_ids.extend(posting.getKeys())
            prev_postings.append(posting)
        # More than 1 token
        else:
            curr_ids = posting.getKeys()
            merge_posting_list(merged_ids, curr_ids, prev_postings)

        if posting is not None:
            for docId in posting.getKeys():
                print "docId", docId
                print "\t", posting.getTf(docId) # returns tf
                print "\t", posting.getPos(docId) # returns list of positions

def main(dictionary_fname, posting_fname, query_fname, output_fname):
    # For each query phrase
    # Split terms 1, 2, 3 (max is 3)
    #  Postings list of t1 merge (AND) with t2
    #  For each match in a docID, check if position matches
    # Result postings list merge with t3
        # Retrieve docsIds for term 1
        # Retrieve docIds for term 2
    with open(dictionary_fname) as dictionary_file:
        with open(posting_fname) as posting_file:
            with open(query_fname) as query_file:
                dictionary = json.load(dictionary_file)
                print dictionary
                for query in query_file:
                    phrases = process_query(query)
                    doc_ids = []
                    for phrase_tokens in phrases:
                        doc_ids.extend(get_doc_ids_for_phrase(phrase_tokens, dictionary, posting_file))


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
