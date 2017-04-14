import re
from xml.etree import ElementTree
import time

"""
This class takes in a file object, reads it and
strips away all css, escape characters, numbers and non-alphanumeric characters
"""
class Cleaner:

    def __init__(self):
        self.content = ''

    def clean(self, fileObj):
        self.content = ''
        self.removeXmlTag(fileObj)
        self.removeEscapeChar()
        self.removeCss()
        self.removeNumbers()
        self.removeNonAlphaNumericChar()
        self.content = ' '.join(self.content.split())
        return self.content

    def removeCss(self):
        start_time = time.time()
        multiLineCssRegex = re.compile(r".+\{\s*(\n.*:.*;?\s*)+\s+\}")
        self.content = multiLineCssRegex.sub("", self.content)

        singleLineCssRegex = re.compile(r".+\{.+:.+;?\s*\}")
        self.content = singleLineCssRegex.sub("", self.content)
        print "Removing CSS took: " + str(time.time()-start_time) + " seconds"

    def removeNumbers(self):
        start_time = time.time()
        self.content = re.sub(r"\d", "", self.content)
        print "Removing Numbers took: " + str(time.time()-start_time) + " seconds"

    def removeEscapeChar(self):
        start_time = time.time()
        entityNameRegex = re.compile(r"&\w+;")
        self.content = entityNameRegex.sub("", self.content)

        entityCodeRegex = re.compile(r"&#\d;")
        self.content = entityCodeRegex.sub("", self.content)
        print "Removing Escape Chars took: " + str(time.time()-start_time) + " seconds"

    def removeNonAlphaNumericChar(self):
        start_time = time.time()
        nonAlphaNumericCharRegex = re.compile(r"[^a-zA-Z0-9 ]")
        self.content = nonAlphaNumericCharRegex.sub(" ", self.content)
        print "Removing Non alphanumeric Chars took: " + str(time.time()-start_time) + " seconds"

    def removeXmlTag(self, fileObj):
        start_time = time.time()
        try:
            tree = ElementTree.parse(fileObj)
            for node in tree.iter():
                # print "Printing xml tag",
                # print node.tag, node.attrib, node.text
                if node.get('name') == "content":
                    self.content = node.text;
                    # print "content", content
                    break;
        except:
            print "EXCEPTION in removeXmlTag, skipping"
            self.content = ""
            # lines = [x for x in file]
            # for line in lines:
            #     self.content += line
        print "Removing XML tag: " + str(time.time()-start_time) + " seconds"
