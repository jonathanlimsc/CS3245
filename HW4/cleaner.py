import re
from xml.etree import ElementTree
import time
import sys

"""
This class takes in a file object, reads it and
strips away all css, escape characters, numbers and non-alphanumeric characters
"""
class Cleaner:

    CHAR_LIMIT = 16000

    def __init__(self):
        self.content = ''

    def clean(self, fileObj):
        self.content = ''
        self.removeXmlTag(fileObj)
        self.removeEscapeChar()
        self.removeNonAlphabeticalChar()
        self.content = ' '.join(self.content.split())
        return self.content

    def removeNumbers(self):
        # start_time = time.time()
        self.content = re.sub(r"\d", "", self.content)
        # print "Removing Numbers took: " + str(time.time()-start_time) + " seconds"

    def removeEscapeChar(self):
        # start_time = time.time()
        entityNameRegex = re.compile(r"&\w+;")
        self.content = entityNameRegex.sub("", self.content)

        entityCodeRegex = re.compile(r"&#\d;")
        self.content = entityCodeRegex.sub("", self.content)
        # print "Removing Escape Chars took: " + str(time.time()-start_time) + " seconds"

    def removeNonAlphabeticalChar(self):
        start_time = time.time()
        nonAlphabeticalRegex = re.compile(r"[^a-zA-Z]")
        # print "Before"
        # print self.content
        # print ""
        self.content = nonAlphabeticalRegex.sub(" ", self.content)
        # print "After"
        # print self.content
        # print "Removing Non alphanumeric Chars took: " + str(time.time()-start_time) + " seconds"

    def removeXmlTag(self, fileObj):
        # start_time = time.time()
        try:
            tree = ElementTree.parse(fileObj)
            for node in tree.iter():
                # print "Printing xml tag",
                # print node.tag, node.attrib, node.text
                if node.get('name') == "content":
                    self.content = node.text[0:Cleaner.CHAR_LIMIT]

                    break
        except Exception as e:
            print "EXCEPTION in removeXmlTag, skipping" + str(sys.exc_info()[0])
            self.content = ""

        # print "Removing XML tag: " + str(time.time()-start_time) + " seconds"
