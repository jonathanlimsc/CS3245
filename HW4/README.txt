This is the README file for A0110839H's and A0163559U's submission

== Python Version ==

We are using Python Version 2.7.11 for this assignment.

== General Notes about this assignment ==


In index.py we now build a document vector and compute document length for each document in the corpus. We also keep track of each term's frequency within each document.

To index the intellex corpus in particular, we decided to use positional indexing by adding a list of indices to the posting class. With knowledge of the location of terms in a document, we are able to support phrasal queries by using a merge algorithm at search time.

Since the corpus documents contain xml tags that are irrelevant to the search, we scan all documents before indexing and use Python's ElementTree to ignore superfluous data, extracting only the content that a user would search for. We clean the content during this scan as well, removing escape characters, css, numbers and non-alpha-numeric characters to clarify search.

We also considered indexing with trigrams because this would provide an improved search speed for phrasal queries, but indexing times were too slow. We tried indexing on tembusu and the ASPIRE 1 supercomputer, but without using multiple processors, indexing such a large corpus was not feasible.

An other compromise we made to increase index speed was to only index the first 10000 characters of each document's content section. This allows our search of the singapore corpus to stay below 20 minutes. Since the files begin with a summary, the impact on recall can be partly minimized.

A0163559U worked primarily on indexing.
A0110839H worked primarily on searching and testing.

== Files included with this submission ==

index.py - Entry point for indexing. Reads the corpus, builds the dictionary and
    posting file, serializes the dictionary.

dictionary.py - Class for dictionary.

postings.py - Class wrapper for handling reading and writing
  posting entries to posting file.

search.py - Entry point for search. Reads and deserializes the dictionary, reads
  the posting file, and writes to the result file.

utils.py - Miscellaneous functions. Currently only holds process_raw_to_token, which takes in raw document text and returns a list of tokens for indexing.

dictionary.txt - Serialized dictionary

postings.txt - Saved posting entries

queries.txt - Some test queries

output.txt - Search output

README.txt - This file.

== Statement of individual work ==

Please initial one of the following statements.

[X] We, A0110839H and A0163559U, certify that we have followed the CS 3245 Information Retrieval class guidelines for homework assignments.  In
particular, we expressly vow that we have followed the Facebook rule
in discussing with others in doing the assignment and did not take notes
(digital or printed) from the discussions.


== References ==

1. Stackoverflow on miscellaneous Python functions

2. Python docs, such as those for heapq
