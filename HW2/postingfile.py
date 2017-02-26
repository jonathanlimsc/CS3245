import os

class PostingFile:
    def __init__(filename, mode):
        self.filename = filename
        self.mode = mode
        self.file_obj = None

    def open(self):
        if self.file_obj is None:
            self.file_obj = open(self.filename, self.mode)

    def close(self):
        if self.file_obj is not None:
            self.file_obj.close()

    def writePostingEntry(self, doc_id, next_ptr, skip_doc_id, skip_ptr, overwrite_pos=None):
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
        posting_entry = PostingEntry.get_entry_instance_from_string(self.file_obj.read(POSTING_ENTRY_SIZE))
        posting_entry.set_posting_file(self.file_obj)

        return posting_entry


class PostingEntry(object):
    POSTING_ENTRY_SIZE = 10 * 4 + 4
    POSTING_STRING_FORMAT = ""

    def __init__(doc_id, next_ptr, skip_doc_id, skip_ptr, posting_file=None):
        self.doc_id = doc_id
        self.next_ptr = next_ptr
        self.skip_doc_id = skip_doc_id
        self.skip_ptr = skip_ptr
    #     self.posting_file = posting_file
    #
    # def set_posting_file(self, posting_file):
    #     if self.posting_file is None:
    #         self.posting_file = posting_file

    def to_string(self):
        return POSTING_STRING_FORMAT % (
            int(self.doc_id),
            int(self.next_ptr),
            int(self.skip_doc_id),
            int(self.skip_ptr)
        )

    def get_entry_instance_from_string(entry_str):
        entry_elements = entry_str.split(' ')
        doc_id = int(entry_elements[0])
        next_ptr = int(entry_elements[1])
        skip_doc_id = int(entry_elements[2])
        skip_ptr = int(entry_elements[3])

        return PostingEntry(doc_id, next_ptr, skip_doc_id, skip_ptr)
