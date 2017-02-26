
import json

class Dictionary:
    def __init__(self):
        self.term_freq_hash = {}
        self.start_ptr_hash = {}
        self.end_ptr_hash = {}
        self.doc_id_hash = {}

    def add_term(self, term, doc_id, ptr):
        '''
        Adds a term from a document
        :param term - The term
        :param doc_id - The id of the document the term came from
        :param ptr - The pointer that the postings list is currently at
        '''
        # New term
        if not self.has_term(term):
            self.doc_id_hash[term] = [doc_id]
            self.term_freq_hash[term] = 1
            self.start_ptr_hash[term] = ptr
            self.end_ptr_hash[term] = ptr
        else:
            # New doc_id for this term
            if doc_id not in self.doc_id_hash[term]:
                self.doc_id_hash[term].append(doc_id)
                self.term_freq_hash[term] += 1
                self.end_ptr_hash[term] = ptr

    def has_term(self, term):
        return term in self.doc_id_hash.keys()

    def has_doc_id(self, term, doc_id):
        return doc_id in self.doc_id_hash[term]

    def get_freq(self, term):
        return self.term_freq_hash[term]

    def get_start_ptr(self, term):
        return self.start_ptr_hash[term]

    def get_end_ptr(self, term):
        return self.end_ptr_hash[term]

    def serializeDict(self):
        dictionary = {}
        for term in self.term_freq_hash.keys():
            dictionary[term] = {
                'f': self.get_freq(term),
                's': self.get_start_ptr(term),
                'e': self.get_end_ptr(term)
            }
        return json.dumps(dictionary)

    # def deserializeDict(self):
d = Dictionary()
d.add_term('hello', 3, 1234)
d.serializeDict();
