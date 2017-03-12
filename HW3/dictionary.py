import cPickle
import json

class Dictionary:
    def __init__(self):
        self.doc_ids = set()
        self.doc_freq_hash = {}
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
        self.doc_ids.add(doc_id)
        # New term
        if not self.has_term(term):
            self.doc_id_hash[term] = [doc_id]
            self.doc_freq_hash[term] = 1
            self.start_ptr_hash[term] = ptr
            self.end_ptr_hash[term] = ptr
        else:
            # New doc_id for this term
            if doc_id not in self.doc_id_hash[term]:
                self.doc_id_hash[term].append(doc_id)
                self.doc_freq_hash[term] += 1
                self.end_ptr_hash[term] = ptr

    def has_term(self, term):
        return term in self.doc_freq_hash.keys()

    def has_doc_id(self, term, doc_id):
        return doc_id in self.doc_id_hash[term]

    def get_freq(self, term):
        return self.doc_freq_hash[term]

    def get_start_ptr(self, term):
        return self.start_ptr_hash[term]

    def get_end_ptr(self, term):
        return self.end_ptr_hash[term]

    def get_all_terms(self):
        return self.doc_freq_hash.keys()

    def serialize_dict(self):
        terms = {}
        for term in self.doc_freq_hash.keys():
            terms[term] = {
                'f': self.get_freq(term),
                's': self.get_start_ptr(term),
                'e': self.get_end_ptr(term)
            }
        dict_repr = {
            'terms': terms,
            'ids': self.doc_ids
        }
        return cPickle.dumps(dict_repr)

    def save_dict_to_file(self, file_path):
        str_repr = self.serialize_dict()
        with open(file_path, 'w+') as f:
            f.write(str_repr)
        f.close()
        return str_repr

    @classmethod
    def load_dict_from_file(cls, file_path):
        with open(file_path, 'r') as f:
            str_repr = ""
            for line in f:
                str_repr += line
        f.close()

        obj = cPickle.loads(str_repr)
        dictionary = cls()
        doc_freq_hash = {}
        start_ptr_hash = {}
        end_ptr_hash = {}
        terms = obj['terms']
        for term in terms.keys():
            freq = terms[term]['f']
            start_ptr = terms[term]['s']
            end_ptr = terms[term]['e']

            doc_freq_hash[term] = freq
            start_ptr_hash[term] = start_ptr
            end_ptr_hash[term] = end_ptr

        dictionary.doc_freq_hash = doc_freq_hash
        dictionary.start_ptr_hash = start_ptr_hash
        dictionary.end_ptr_hash = end_ptr_hash
        dictionary.doc_ids = obj['ids']

        return dictionary
