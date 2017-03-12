This is the README file for A0110839H's submission

== Python Version ==

I'm using Python Version 2.7.11 for
this assignment.

== General Notes about this assignment ==



== Files included with this submission ==

index.py - Entry point for indexing. Reads the corpus, builds the dictionary and
    posting file, serializes the dictionary.

dictionary.py - Class for dictionary.

postingfile.py - Class wrapper for handling reading and writing
  posting entries to posting file.

search.py - Entry point for search. Reads and deserializes the dictionary, reads
  the posting file, and writes to the result file.

query_parser.py - Converts a query into post-fix formatted tokens.

boolops.py - Contains functions to handle the boolean operations between posting
  lists and/or intermediate results

utils.py - Miscellaneous functions. Currently only holds normalize_token. This is
  such that future modification to normalizing can be done from a single point.

dictionary.txt - Serialized dictionary

postings.txt - Saved posting entries

queries.txt - Some test queries

output.txt - Search output

README.txt - This file.

ESSAY.txt - My answers to essay questions.

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0110839H, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.


== References ==

1. ymichael's Github repository for architecture and ideas on building the
postings list on file
https://github.com/ymichael/cs3245-hw/tree/master/hw2

2. Stackoverflow on miscellaneous Python functions

3. Python docs
