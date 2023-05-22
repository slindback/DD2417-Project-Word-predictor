# Written by Simon Lindbäck and Anton Lewander
from collections import defaultdict
import argparse
import codecs
import string
import math
import json
import nltk
import os

class BigramTrainer(object):
    """
    This class constructs a bigram language model from a corpus.
    """

    def __init__(self, path):
        self.file_path = path
        self.i2w = {}
        self.w2i = {}
        self.unigram_count = defaultdict(int)
        self.bigram_count = defaultdict(lambda: defaultdict(int))
        self.unique_words = 0
        self.total_words = 0
        self.laplace_smoothing = False

    def process_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as text_file:
            text = reader = str(text_file.read()).lower()
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

def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='BigramTrainer')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file from which to build the language model')
    parser.add_argument('--destination', '-d', type=str, help='file in which to store the language model')

    arguments = parser.parse_args()

    if arguments.destination and not os.path.exists(arguments.destination):
        bigram_trainer = BigramTrainer(arguments.file)

        bigram_trainer.process_file()

        stats = bigram_trainer.stats()
        with codecs.open(arguments.destination, 'w', 'utf-8' ) as f:
            for row in stats: f.write(row + '\n')
    else:
        print("A language model for {} already exists".format(arguments.file))

if __name__ == "__main__":
    main()
