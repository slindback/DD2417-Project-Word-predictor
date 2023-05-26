import argparse
import os
import sys
from data.sources.test_sentences_sample import sentences
from RNN import main as rnn_main

def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='RNN')
    parser.add_argument('--file', '-f', type=str, required=True, help='file used to train language model')
    parser.add_argument('--destination', '-d', type=str, help='file in which to store the language model')
    parser.add_argument('--epochs', '-e', type=int, default=1, help='number of epochs for training')

    arguments = parser.parse_args()

    # Call RNN.py with the command-line arguments
    sentence = ["I","am"]
    predicted_words = rnn_main(sentence)
    print("Predicted next words:", predicted_words)

if __name__ == "__main__":
    main()
