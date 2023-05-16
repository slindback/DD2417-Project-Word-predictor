# Written by Simon Lindbäck and Anton Lewander
from collections import defaultdict
import math
import json
import nltk

class BigramTrainer(object):
    """
    This class constructs a bigram language model from a corpus.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.i2w = {}
        self.w2i = {}
        self.unigram_count = defaultdict(int)
        self.bigram_count = defaultdict(lambda: defaultdict(int))
        self.unique_words = 0
        self.total_words = 0
        self.laplace_smoothing = False

    def process_file(self):
        with open(self.file_path) as file:
            data = json.load(file)
        messages = data['smsCorpus']['message']
        text = ''
        for i in range(len(messages)):
            text += str(messages[i]['text']['$']).lower()
        try :
            self.tokens = nltk.word_tokenize(text) # Important that it is named self.tokens for the --check flag to work
        except LookupError :
            nltk.download('punkt')
            self.tokens = nltk.word_tokenize(text)
        for token in self.tokens:
            self.process_token(token)

    def process_token(self, token):
        """
        Processes one word in the training corpus, and adjusts the unigram and
        bigram counts.
        """
        if token not in self.w2i:
            self.w2i[token] = len(self.w2i)
            self.i2w[len(self.i2w)] = token
            self.unigram_count[token] = 0
            self.unique_words += 1
        self.unigram_count[token] += 1
        self.total_words += 1

        if self.unique_words > 1:
            self.bigram_count[self.w2i[self.tokens[self.total_words-2]]][self.w2i[token]] += 1
            """ bigram_count[index för förgående token][index för nuvarande token] += 1 """

    def stats(self):
        rows_to_print = []
        rows_to_print.append(str(self.unique_words)+' '+str(self.total_words))

        for word in self.w2i:
            rows_to_print.append(str(self.w2i[word])+' '+word+' '+str(self.unigram_count[word]))

        for index in range(self.unique_words-1):
            for next_index in self.bigram_count[index]:
                p = (self.bigram_count[index][next_index]/self.unigram_count[self.i2w[index]])
                rows_to_print.append(str(index)+' '+str(next_index)+' '+str('{:.15f}'.format(math.log(p))))

        rows_to_print.append('-1')
        return rows_to_print
    """
    def read_json(path):
        with open(path) as file:
            data = json.load(file)
        for i in range(len(messages)):
            yield clean_line(messages[i]['text']['$']):

    import string
        def clean_line(self, line):
            clean_str, clean_line = "", []
            line = str(line).lower()
            for word in line:
                if not (word in string.punctuation or word in string.digits):
                    clean_str += word
            clean_line = clean_str.split()
            return clean_line
    """
