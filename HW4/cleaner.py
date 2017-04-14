import re
from xml.etree import ElementTree

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
        multiLineCssRegex = re.compile(r".+\{\s*(\n.*:.*;?\s*)+\s+\}")
        self.content = multiLineCssRegex.sub("", self.content)

        singleLineCssRegex = re.compile(r".+\{.+:.+;?\s*\}")
        self.content = singleLineCssRegex.sub("", self.content)

    def removeNumbers(self):
        self.content = re.sub(r"\d", "", self.content)

    def removeEscapeChar(self):
        entityNameRegex = re.compile(r"&\w+;")
        self.content = entityNameRegex.sub("", self.content)

        entityCodeRegex = re.compile(r"&#\d;")
        self.content = entityCodeRegex.sub("", self.content)

    def removeNonAlphaNumericChar(self):
        nonAlphaNumericCharRegex = re.compile(r"[^a-zA-Z0-9 ]")
        self.content = nonAlphaNumericCharRegex.sub(" ", self.content)

    def removeXmlTag(self, fileObj):
        try:
            tree = ElementTree.parse(fileObj)
            for node in tree.iter():
                print "Printing xml tag",
                print node.tag, "attr:", str(node.attrib)#, node.text
                self.content += node.text + " "
                if node.get('name') == "content":
                    # print "BREAK HERE"
                    break;
        except:
            print "EXCEPTION in removeXmlTag, skipping"
            self.content = ""
            # lines = [x for x in file]
            # for line in lines:
            #     self.content += line
