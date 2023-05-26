# Written by Simon Lindbäck and Anton Lewander
from collections import defaultdict
import argparse
import random
import codecs
import math
import os
#import heapq

class Predictor(object):
    """
    This class makes word predictions based on a bigram language model.
    """
    def __init__(self, path, predictions=3):
        self.model_path = path
        self.i2w = {}
        self.w2i = {}
        self.unigram_count = defaultdict(int)
        self.bigram_count = defaultdict(lambda: defaultdict(int))
        self.bigram_prob = defaultdict(dict)
        self.unique_words = 0
        self.total_words = 0
        self.number_of_predictions = predictions

    def read_model(self):
        try:
            with codecs.open(self.model_path, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))
                for line in range(self.unique_words):
                    data = f.readline().strip().split(' ')
                    i2w, word, occur = int(data[0]), data[1], int(data[2])
                    self.unigram_count[word] = occur
                    self.w2i[word] = len(self.w2i)
                    self.i2w[len(self.i2w)] = word

                while True:
                    data = f.readline().strip().split(' ')
                    if data == ['-1']: break
                    index, next_index, log_prob = int(data[0]), int(data[1]), float(data[2])
                    self.bigram_prob[index][next_index] = log_prob
                return True

        except IOError:
            print("Couldn't find bigram probabilities file {}".format(self.model_path))
            return False

    def predict(self, w):
        """
        Generates and prints n predictions by sampling from the distribution of the language model.
        """
        w=w.lower()
        predictions = []

        for word in range(self.number_of_predictions):
            if self.w2i[w] in self.bigram_prob:
                distr = {key: math.exp(value) for key, value in self.bigram_prob[self.w2i[w]].items()}
                outcomes, weights = zip(*distr.items())
                prediction = self.i2w[random.choices(outcomes, weights=weights)[0]]

            else: prediction = random.choice(list(self.i2w.values()))
            if prediction not in predictions: predictions.append(prediction)
        return predictions

def main():
    """
    TAKES WORD THROUGH COMMAND LINE AND PRINTS PREDICTIONS
    ------------------------------------------------------------------------
    """
    parser = argparse.ArgumentParser(description='BigramTester')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file with language model')
    parser.add_argument('--word', '-w', type=str, required=True, help='word')
    parser.add_argument('--predictions', '-n', type=int, default=3)

    arguments = parser.parse_args()

    predictor = Predictor(arguments.file,arguments.predictions)
    predictor.read_model()
    predictions = predictor.predict(arguments.word)
    print(predictions)

if __name__ == "__main__":
    main()
