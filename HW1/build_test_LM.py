#!/usr/bin/python
import re
import nltk
import sys
import getopt
import utils
import langmodel

NGRAM_WINDOW = 4

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print 'building language models...'

    universal_ngrams = set()
    lang_models = {}
    with open(in_file) as input_fs:
        for line in input_fs:
            # Splits line into <language><string>
            arr = line.split(" ", 1)
            lang = arr[0]
            string = arr[1]

            # Instantiate language models
            lang_models.setdefault(lang, langmodel.LanguageModel(lang))

            # Clean string of symbols
            processed_str = utils.normalize(string)

            # Tokenize clean string into n-grams with padding
            ngram_arr = utils.tokenize(processed_str, NGRAM_WINDOW)

            # Add n-grams into LM and universal set
            lm = lang_models[lang]
            for ngram in ngram_arr:
                universal_ngrams.add(ngram)
                lm.incrementNgram(ngram)

    # Add set tokens into all LMs to achieve parity in n-grams
    for lang in lang_models:
        lm = lang_models[lang]
        for ngram in universal_ngrams:
            lm.addNgramWithSmoothing(ngram)
        lm.convertCountsToProb()

    print "Checking lang models..."
    for lang in lang_models:
        lm = lang_models[lang]
        print lm
        print lm.lang
        print lm.total_count

    return lang_models

def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print "testing language models..."
    with open(in_file, 'r') as in_f:
        for line in in_f:
            processed_str = utils.normalize(line)
            ngram_arr = utils.tokenize(line, NGRAM_WINDOW)

            prediction = None
            highest_prob = float("-inf")
            for lang in LM:
                model = LM[lang]
                result = model.evalProbability(ngram_arr)
                print "Probability of " + lang + ": " + str(result)
                if result > highest_prob:
                    highest_prob = result
                    prediction = lang
            if highest_prob == 0:
                prediction = "other"

            print "     Prediction: " + prediction
            with open(out_file, 'a') as out_f:
                output = prediction + " " + line
                out_f.write(output)
            out_f.close
    in_f.close()
def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
