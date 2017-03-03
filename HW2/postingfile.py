import os

INVALID_CONST = -1

class PostingFile(object):
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file_obj = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type=None, value=None, traceback=None):
        self.close()

    def open(self):
        if self.file_obj is None:
            self.file_obj = open(self.filename, self.mode)

    def close(self):
        if self.file_obj is not None:
            self.file_obj.close()

    def write_posting_entry(self, doc_id, next_ptr=INVALID_CONST, skip_doc_id=INVALID_CONST, skip_ptr=INVALID_CONST, overwrite_pos=None):
        '''
        Write posting entry at end of file if no overwrite position is given. If given, the entry
        will be written at the given byte position.
        :params doc_id - document id
        :params next_ptr - pointer of the next entry
        :params skip_doc_id - document id that will be skipped to
        :params skip_ptr - pointer of entry to be skipped to
        '''
        if overwrite_pos is None:
            self.file_obj.seek(0, os.SEEK_END)
        else:
            self.file_obj.seek(overwrite_pos, os.SEEK_SET)

        self.file_obj.write(PostingEntry(doc_id, next_ptr, skip_doc_id, skip_ptr).to_string())

    def read_posting_entry(self, byte_pos):
        '''
        Reads the posting entry at the provided byte position
        :params byte_pos - Byte position in the file
        '''
        if self.file_obj is None:
            return None
        self.file_obj.seek(byte_pos)
        posting_entry = PostingEntry.get_entry_instance_from_string(self.file_obj.read(PostingEntry.POSTING_ENTRY_SIZE))

        return posting_entry

    def get_posting_list_for_ptr(self, ptr):
        '''
        Returns a posting list for given term.
        '''
        if self.file_obj is None:
            return []
        p_list = []
        p = self.read_posting_entry(ptr)

        while p is not None:
            p_list.append(p)
            p = self.get_next_entry(p)

        return p_list

    def get_next_entry(self, entry):
        pos = entry.next_ptr
        if pos == -1:
            return None

        return self.read_posting_entry(pos)

    def get_skip_entry(self, entry):
        pos = entry.skip_ptr
        if pos == -1:
            return None

        return self.read_posting_entry(pos)

class PostingEntry(object):
    POSTING_ENTRY_SIZE = 10 * 4 + 4
    POSTING_STRING_FORMAT = "%010d %010d %010d %010d\n"

    def __init__(self, doc_id, next_ptr, skip_doc_id, skip_ptr):
        self.doc_id = doc_id
        self.next_ptr = next_ptr
        self.skip_doc_id = skip_doc_id
        self.skip_ptr = skip_ptr

    def to_string(self):
        return PostingEntry.POSTING_STRING_FORMAT % (
            int(self.doc_id),
            int(self.next_ptr),
            int(self.skip_doc_id),
            int(self.skip_ptr)
        )

    @classmethod
    def get_entry_instance_from_string(cls, entry_str):
        entry_elements = entry_str.split(' ')
        doc_id = int(entry_elements[0])
        next_ptr = int(entry_elements[1])
        skip_doc_id = int(entry_elements[2])
        skip_ptr = int(entry_elements[3])

        return cls(doc_id, next_ptr, skip_doc_id, skip_ptr)
