# This summarizer code is a modified version of a previous project of mine.
# As per the rules none of this is directly copied over.

import numpy as np
import re
from parse_words import *


stop_words = ["", " ", "\n", "i", "me", "my", "oh", 'mr', 'mrs', 'ms', 'dr', 'said', "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


# THis class wants an input in the form of sentences from the parser file
class Summarizer(object):
    word_endings = [' ', '-', '--', '.', '!', '?']  # regex would be nice here

    def __init__(self, sentences, title=""):
        self.total_words = 0
        self.sentences = sentences
        self.words = {}
        if len(title) > 0:
            self.title = title.lower().split(' ')
        else:
            self.title = []

    def eval_sentences(self):
        for s in self.sentences:
            if s.text[-1] == '!':
                s.val = 2
            elif s.text[-1] == '?':
                s.val = 2
            else:
                s.val = 0
            for word in re.split(' |-', s.text):
                # Add word to total. Used to find the desired output size
                self.total_words += 1
                # Count number of each word
                if word not in stop_words:
                    if word in self.words:
                        self.words[word] += 1
                    else:
                        self.words[word] = 1

        # This is copied over as much of it has already been optimized
        # These variables represent the adjustments. all fractional point are rounded down
        std_mult = 1  # How many point a word get for each standard deviation above occurrences mean it is
        under_mean = 1  # For any word with number of occurrences bellow the mean, this is added
        per_word = 0  # baseline number of points added for every word
        char_mult = 1/3  # For every character in a word above 6 character it will receive this many points.
        title_word = 3  # Additional points if word is in the title
        word_thres = 5  # Only sentences with this many or more words will be considered
        sw_val = 0  # Number of points a sentence gets for each stop word

        mean = np.array([self.words[k] for k in self.words]).mean()
        mean_squared = np.array([self.words[k]*self.words[k] for k in self.words]).mean()
        # For some reason this gave me slightly different values than np.std, probably just a rounding issue
        std = np.sqrt(mean_squared - mean)
        for word in self.words:
            if self.words[word] < mean + std or std == 0.0:
                self.words[word] = max(0, int(char_mult * (len(word)-6))) + under_mean + per_word
            else:
                self.words[word] = int(std_mult * ((self.words[word] - mean)/std)) + \
                                   max(0, int(char_mult * (len(word)-6))) + per_word

        # We want to consider the title too. we will give an addition amount of points for words in the title.
        for w in self.title:
            if w in self.words:
                self.words[w] += title_word

        # now we want to give each sentence its own value
        for s in self.sentences:
            if s.length < word_thres:
                s.val = 0
                continue
            for w in re.split(' |-', s.text):
                # For each word in the sentence we add the value
                if w not in stop_words:
                    if w in self.words:
                        s.val += self.words[w]
                    else:
                        # this should never happen. If it does its treated as a stop word
                        print('*** Word not found: ' + w)
                        s.val += sw_val
                else:
                    s.val += sw_val

    def create_summary(self, percent_words=0.0, num_words=0):
        if percent_words == 0 and num_words == 0:
            return "Error: summary size not specified"
        # parse data to get points for each sentence
        self.eval_sentences()
        if percent_words != 0.0:
            return self.opt_summary(self.sentences, int(percent_words*self.total_words))
        else:
            return self.opt_summary(self.sentences, num_words)

    @staticmethod
    def opt_summary(sentence_arr, num_words):
        def recover_solution(i, j):
            solution = []
            while i > 0 and j > 0:
                if opt[i, j] == opt[i-1, j]:
                    i -= 1
                else:
                    solution.append(sentence_arr[i-1])
                    j -= sentence_arr[i-1].length
                    i -= 1
            return solution[::-1]

        # This initializes our base cases to 0. Because we iterate through all items everything can be zero
        opt = np.array([[0 for _ in range(num_words + 1)] for _ in range(len(sentence_arr) + 1)])
        # This initializes our base cases

        for i in range(1, len(sentence_arr) + 1):
            for j in range(1, num_words + 1):
                # It is important to not that every time we access the opt array we use i and j and ever time
                # we access the w_arr ir v_arr we use i-1 or j-1. This is because item 1 is index 0.
                if j - sentence_arr[i-1].length >= 0:
                    opt[i, j] = max(opt[i - 1, j], opt[i - 1, j - sentence_arr[i-1].length] + sentence_arr[i-1].val)
                else:
                    opt[i, j] = opt[i - 1, j]
        return recover_solution(len(sentence_arr), num_words)


def test_thing(s):
    print(s)


if __name__ == '__main__':
    parse_words.test("TEST ")
