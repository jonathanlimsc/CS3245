class Posting(object):
    """
    dict stores {docId: weightedtf, docId: weightedtf, ..}
    """
    def __init__(self, docId=None, weightedtf=0):
        self.tf = {}
        self.positions = {}
        self.docIds = []
        if docId is not None:
            self.docIds.append(docId)
            self.tf[docId] = weightedtf
            self.positions[docId] = []

    def add(self, docId, weightedtf):
        if docId not in self.docIds:
            self.docIds.append(docId)
        self.tf[docId] = weightedtf

    def addPos(self, docId, pos):
        if docId not in self.positions:
            # resolves case where term appears multiple times in a doc
            self.positions[docId] = []
        self.positions[docId].append(pos)


    def getTf(self, docId): # get tf
        return self.tf[docId]

    def getPos(self, docId): # get list of positions where term appears in docId
        return self.positions[docId]

    def getKeys(self): # get list of docs where this term appears (Not sorted)
        return self.tf.keys()

    def getDocIds(self): # get list of doc ids where this term appears (Sorted order)
        return self.docIds

    def updateTf(self, docId, newtf):
        self.tf[docId] = newtf

    def __str__(self):
        string = ""
        for k, v in self.tf.iteritems():
            string += (  '(' + str(k) + ',' + str(v) + '), '  )
        return string
