from data.sources.test_sentences_sample import sentences
from RNN import main as rnn_main
from datetime import datetime
import argparse
import sys
import os

def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='RNN')
    parser.add_argument('--file', '-f', type=str, required=True, help='file used to train language model')
    parser.add_argument('--destination', '-d', type=str, help='file in which to store the language model')
    parser.add_argument('--epochs', '-e', type=int, default=1, help='number of epochs for training')

    arguments = parser.parse_args()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Starting at ", current_time)

    # s: number of words to send to the RNN predictor. Range 1 to 16
    # (16 is the length of the longest sentence in the test set)
    for s in range(1,17):
        strokes_saved = 0
        total_chars = 0
        for sentence in sentences:
            sentence = sentence.split()
            total_chars += sum(len(word) for word in sentence)
            for i in range(1,len(sentence)):
                if i-s > -1: predicted_words = rnn_main(sentence[i-s:i],arguments.file,arguments.destination,arguments.epochs)
                else:        predicted_words = rnn_main(sentence[:i],arguments.file,arguments.destination,arguments.epochs)
                if sentence[i] in predicted_words:
                    strokes_saved += len(sentence[i])

        percentage = str(round((strokes_saved / total_chars) * 100, 2))
        print("{} keystrokes saved with {}. {} words sent to predictor. Percentage: {}%".format(strokes_saved, arguments.destination, s, percentage))

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Ending at ", current_time)

if __name__ == "__main__":
    main()
