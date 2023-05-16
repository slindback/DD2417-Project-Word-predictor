# Written by Simon Lindbäck and Anton Lewander
from BigramTrainer import BigramTrainer

import argparse
import operator
import os
"""
def clean_line(line):
    clean_str, clean_line = "", []
    line = str(line).lower()
    for word in line:
        if not (word in string.punctuation or word in string.digits):
            clean_str += word
    clean_line = clean_str.split()
    return clean_line

def read_json(path):
    with open(path) as file:
        data = json.load(file)
    for i in range(len(messages)):
        yield clean_line(messages[i]['text']['$']):
"""

def main():
    """
    Parse command line arguments
    """
    """
    parser = argparse.ArgumentParser(description='BigramTrainer')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file from which to build the language model')
    parser.add_argument('--destination', '-d', type=str, help='file in which to store the language model')
    arguments = parser.parse_args()

    bigram_trainer = BigramTrainer()

    bigram_trainer.process_files(arguments.file)

    stats = bigram_trainer.stats()
    if arguments.destination:
        with codecs.open(arguments.destination, 'w', 'utf-8' ) as f:
            for row in stats: f.write(row + '\n')
    else:
        for row in stats: print(row)
    """
    current_dir = os.getcwd()
    json_path = os.path.join(current_dir,'data', 'smsCorpus_en_2015.03.09_all.json')
    bigram_trainer = BigramTrainer(json_path)
    bigram_trainer.process_file() # Calculating unigram and bigram counts
    stats = bigram_trainer.stats() # Get bigram stats
    stats_path = os.path.join('data', 'stats.txt')
    if not os.path.exists(stats_path):
        os.makedirs('data', exist_ok=True)
        with open(stats_path,'w',encoding='utf-8') as file:
            for row in stats: file.write(row + '\n')

    #unigram_count = {}
    #for sentence in read_json(json_path):
    #    for word in sentence:
    #        if word not in unigram_count:
    #            unigram_count[word] = 1
    #        else: unigram_count[word] +=1


if __name__ == "__main__":
    main()
