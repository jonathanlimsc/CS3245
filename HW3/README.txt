This is the README file for A0110839H's submission

== Python Version ==

I'm using Python Version 2.7.11 for
this assignment.

== General Notes about this assignment ==

I could not submit in time due to a hectic schedule for mid-terms, other project
modules and internship interviews (I've only had about 2 days to work on this). I'm not requesting to be excused, but I was
in progress to submit by 4am, 4 Mar when the comp.nus.edu server went down at
around 3+am. I could not access CS3245's HW2 requirements and was delayed in
answering the essay questions. I would like to request to be graded based on
submission within 5 hours of being late.

My approach is simple and unoptimised due to time constraints. If I were to spend
more time on optimization, I would optimize AND NOT queries and perhaps explore caching
of queries. Searching is also currently done naively according to the post-fix order of the query.
Term frequencies were not used to decide on the ordering of the sub-queries.

Skip pointers were added at the end after an end-to-end test of indexing and search
was done. The skip pointers and skip doc id are stored for each posting entry in the posting file.
If a particular entry has no skip pointer, the pointer and skip doc id will be -1.
I implemented it as such as opposed to iterating with a skip in the program because I wanted
to create a data structure that can allow for actual skipping by reading of the stored data. This
is reminiscent of what I learnt about memory and storage in CS2106 and this seems to be a
basic version of what goes in real operating systems, so that was fun to do. It also might be the case
that in a different program, it has no understanding of the skip length, so with that constraint
in mind, I chose to find a way to implement skipping via a stored pointer in the file.

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

2. Shunting Yard algorithm
https://www.youtube.com/watch?v=QzVVjboyb0s

3. Stackoverflow on miscellaneous Python functions

4. Python docs

5. Stop words
http://xpo6.com/list-of-english-stop-words/
