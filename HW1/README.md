# General Notes about this assignment

This language predictor is made up of :

	1. build_test_LM
	2. LanguageModel class
	3. utils module

In build_test_LM, the function build_LM will read the given file line-by-line, instantiating a new language model if the language is new.
The language string portion of the line will normalized (with options for case-folding and removal of numbers and symbols), and then tokenized into ngrams (with options to specify the window size, via the constant NGRAM_WINDOW). All ngrams generated will be added into a set, universal_ngrams. Ngrams specific to the language will be added to the respective language model. When all lines in the file have been processed, the program does a single pass through universal_ngrams, adding the ngram into each language model if it is unseen (with add-1 smoothing). My algorithm for this process has not been optimized so it may run abit slowly. Then, each language model converts its own dictionary of ngrams:counts to ngrams:probabilities. Finally, the function then passes a dictionary containing the language models to test_LM.

In test_LM, lines are read from the input test file, which go through the same process of normalizing and tokenizing into ngrams. These ngrams will be saved in ngram_arr, which is then passed to each language model via evalProbability(), which sums up the logarithm of probabilties of all matching ngrams. It also calculates the number of unseen ngrams, and if the unseen ngrams to ngrams supplied ratio crosses a threshold (UNSEEN_THRESHOLD) of 0.65, the language model outputs 0, signifying an unknown language. 0.65 was obtained via experimentation. There were two test cases that were correctly predicted as known, with a ratio of 0.47. Other cases of correctly predicted unknown language had ratios of 0.8 and 1.0. Hence I picked 0.65 to prevent oversensitivity to a badly matching but otherwise known language.


# Files included with this submission

## ESSAY.txt
	Contains my answers to the essay questions

## README.txt
	What you are reading now.

## build_test_LM.py
 	The script to execute for building language models and generating predictions.

## eval.py
	Unchanged. Evaluates the accuracy of predictions.

## langmodel.py
	LanguageModel class that holds the data and functions of a language model.

## utils.py
	Basic utilities for normalizing and tokenizing.
