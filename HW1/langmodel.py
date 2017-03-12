import math

class LanguageModel:
    UNSEEN_THRESHOLD = 0.65

    def __init__(self, lang):
        self.lang = lang
        self.ngrams = {}
        self.total_count = 0

    def incrementNgram(self, ngram, increment=1):
        # In the case that the ngram has not been added
        self.ngrams.setdefault(ngram, 0)
        self.ngrams[ngram] += increment

    def addNgramWithSmoothing(self, ngram, smoothing=1):
        '''
        Adds ngram into dict if it does not already exist, with a count equals to smoothing constant.
        '''
        if self.ngrams.has_key(ngram) is False:
            self.incrementNgram(ngram, smoothing)
            for key in self.ngrams:
                # Skip the ngram we just added into self.ngram with smoothing
                if key == ngram:
                    continue
                self.ngrams[key] += smoothing

    # Private method, not to be called externally.
    # Called once to convert ngram counts to probabilities.
    def _totalCount(self):
        '''
        Sums up counts for all ngrams in dictionary before being converted to probability
        '''
        count = 0
        for ngram in self.ngrams:
            count += self.ngrams[ngram]

        self.total_count = count
        return count

    def convertCountsToProb(self):
        totalCount = self._totalCount()
        for ngram in self.ngrams:
            count = self.ngrams[ngram]
            self.ngrams[ngram] = float(count) / totalCount

    def evalProbability(self, ngram_arr):
        unseen_count = 0
        found_count = 0
        found_prob = 0
        total_count = self.total_count

        # Sanity check
        if total_count < 1:
            return 0;

        for ngram in ngram_arr:
            if self.ngrams.has_key(ngram):
                # log(a*b) = log(a) + log(b). We want to find the logarithm of product of probabilities
                # which is equal to the sum of logarithms of probabilities.
                found_prob += math.log(self.ngrams[ngram])
                found_count += 1
            else:
                unseen_count += 1

        print "Unseen-ngram supplied ratio: " + str(float(unseen_count)/len(ngram_arr))
        # More sanity checks
        if found_count < 1 or (float(unseen_count) / len(ngram_arr)) > LanguageModel.UNSEEN_THRESHOLD:
            print "Found count too low, or unseen count too high"
            return 0

        return found_prob

if __name__ == '__main__':
    lm = LanguageModel('bahasa')
    lm.incrementNgram(' bas')
    lm.addSmoothingNgram('hes ')
    print lm.lang
    print lm.ngrams
