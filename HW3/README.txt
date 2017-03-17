This is the README file for A0110839H's and A0163559U's submission

== Python Version ==

We are using Python Version 2.7.11 for
this assignment.

== General Notes about this assignment ==

For this assignment we modified index.py and search.py.
In index.py we now build a document vector and compute document length for each document in the corpus. We also keep track of each term's frequency within each document.

We modified search.py to assign weights to each document matching the query and then return at most the ten most relevant documents.

We decided to remove terms from the query vector if either (1) they were not present or (2) they were present in all documents of the corpus. For terms absent from the dictionary this is a simple choice because the term would not affect any document weights. For terms present in all documents, we decided to eliminate them from the query in part because that query term's weight would be 0, leading to futile adds and multiplies in the future if left in the vector.

== Files included with this submission ==

index.py - Entry point for indexing. Reads the corpus, builds the dictionary and
    posting file, serializes the dictionary.

dictionary.py - Class for dictionary.

postingfile.py - Class wrapper for handling reading and writing
  posting entries to posting file.

search.py - Entry point for search. Reads and deserializes the dictionary, reads
  the posting file, and writes to the result file.

utils.py - Miscellaneous functions. Currently only holds normalize_token. This is
  such that future modification to normalizing can be done from a single point.

dictionary.txt - Serialized dictionary

postings.txt - Saved posting entries

queries.txt - Some test queries

output.txt - Search output

README.txt - This file.

ESSAY.txt - Our answers to essay questions.

== Statement of individual work ==

Please initial one of the following statements.

[X] We, A0110839H and A0163559U, certify that we have followed the CS 3245 Information Retrieval class guidelines for homework assignments.  In
particular, we expressly vow that we have followed the Facebook rule
in discussing with others in doing the assignment and did not take notes
(digital or printed) from the discussions.


== References ==

1. Stackoverflow on miscellaneous Python functions

2. Python docs, such as those for heapq

3. Phrasal queries: http://people.eng.unimelb.edu.au/tcohn/comp90042/l3.pdf

4. Weighting methods: http://acl-arc.comp.nus.edu.sg/archives/acl-arc-090501d3/data/pdf/anthology-PDF/H/H93/H93-1070.pdf
