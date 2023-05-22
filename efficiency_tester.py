from Predictor import Predictor
import test_sentences_sample
import argparse
import os

print_list = []
sentences = test_sentences_sample.sentences

def test_efficiency(path, iterations):
    predictor = Predictor(path)
    predictor.read_model()
    strokes_saved = 0
    total_chars = 0
    for it in range(iterations):
        for sentence in sentences:
            sentence = sentence.split()
            total_chars += sum(len(word) for word in sentence)
            for i in range(len(sentence)):
                predictions = predictor.predict(sentence[i])
                if i+1 in range(len(sentence)):
                    if sentence[i+1] in predictions:
                        strokes_saved += len(sentence[i+1])
    percentage = str(round((strokes_saved / total_chars) * 100, 2))

    return "{} keystrokes saved with {}. Percentage: {}%".format(strokes_saved, os.path.basename(path), percentage)

def main():
    parser = argparse.ArgumentParser(description='BigramTrainer')
    parser.add_argument('--models', '-m', type=str, required=True, help='folder hosting models you want to test')
    parser.add_argument('--destination', '-d', type=str, help='file in which to store stats')
    parser.add_argument('--iterations', '-i', type=int, default=1, help='times the test should run')
    arguments = parser.parse_args()

    with open(arguments.destination, 'w') as output_file:
        output_file.write("Results from {} iteration(s) over {} sentences\n".format(arguments.iterations, len(sentences)))
        output_file.write("----------------------------------------------------------\n")
        for file_name in os.listdir(arguments.models):
            if os.path.isfile(os.path.join(arguments.models, file_name)):
                path = os.path.join(arguments.models, file_name)
                result = test_efficiency(path,arguments.iterations)
                output_file.write(result + "\n")

if __name__ == "__main__":
    main()
