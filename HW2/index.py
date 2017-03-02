import getopt
import sys
import os
from os.path import isfile, join, basename
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from dictionary import Dictionary
from postingfile import PostingFile

def build_index(dir_of_docs, dict_file, postings_file):
    docs = [f for f in os.listdir(dir_of_docs) if isfile(join(dir_of_docs, f)) and f.isdigit()]
    print docs
    sorted_doc_ids = sorted(docs, key=lambda x: int(basename(x)))
    print sorted_doc_ids
    dictionary = Dictionary()
    with PostingFile(postings_file, 'w+') as p_file:
        for doc_id in sorted_doc_ids:
            doc_path = dir_of_docs + '/' + doc_id
            terms = process_file(doc_path)
            print terms
            print "There are " + str(len(terms)) + " terms"
            for term in terms:
                p_file.file_obj.seek(0, os.SEEK_END)
                curr_ptr = p_file.file_obj.tell()

                doc_id = int(doc_id)

                if dictionary.has_term(term):
                    # Overwrite previous posting entry for the term
                    prev_entry_ptr = dictionary.end_ptr_hash[term]
                    prev_entry = p_file.read_posting_entry(prev_entry_ptr)
                    p_file.write_posting_entry(prev_entry.doc_id, curr_ptr, overwrite_pos=prev_entry_ptr)

                # Write new entry to posting file at end
                p_file.write_posting_entry(doc_id)

                dictionary.add_term(term, doc_id, curr_ptr)

        print_term_to_postings(dictionary, p_file)

def print_term_to_postings(dictionary, p_file):
    # Read postings list to test for correctness
    print str(len(dictionary.term_freq_hash.keys())) + " terms in dictionary"
    for term in dictionary.term_freq_hash.keys():
        start_ptr = dictionary.start_ptr_hash[term]
        next_ptr = start_ptr
        print "term is " + term + " "
        doc_ids = []
        while next_ptr != -1:
            pe = p_file.read_posting_entry(next_ptr)
            next_ptr = pe.next_ptr
            doc_ids.append(pe.doc_id)
        print doc_ids
        print dictionary.term_freq_hash[term]

def process_file(doc_path):
    with open(doc_path, 'r') as doc:
        terms = set()
        for line in doc:
            tokens = tokenize(line)
            for term in normalize_tokens(tokens):
                terms.add(term)
        print terms
        print " "
    doc.close()
    return list(terms)

def tokenize(doc_string):
    tokens = []
    for sentence in sent_tokenize(doc_string):
        tokens.extend(word_tokenize(sentence))
    return tokens

def normalize_tokens(tokens):
    '''
    Case folding and stemming
    '''
    stemmer = PorterStemmer()
    result = [stemmer.stem(token.lower()) for token in tokens if len(token) > 0]

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
