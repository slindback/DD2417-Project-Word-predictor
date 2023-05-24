import torch
import torch.nn as nn
import numpy as np
import more_itertools as mit

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        sentences = file.read().splitlines()

    # Tokenize sentences into words
    tokenized_sentences = [sentence.split() for sentence in sentences]

    # Create vocabulary
    vocabulary = set([word for sentence in tokenized_sentences for word in sentence])
    word_to_index = {word: i for i, word in enumerate(vocabulary)}
    index_to_word = {i: word for word, i in word_to_index.items()}

    return tokenized_sentences, word_to_index, index_to_word

def create_training_data(tokenized_sentences, word_to_index, max_len_sentence):
    X = []
    y = []

    for sentence in tokenized_sentences:
        for i in range(len(sentence) - max_len_sentence):
            input_sequence = sentence[i:i+max_len_sentence]
            output_word = sentence[i+max_len_sentence]
            X.append([word_to_index[word] for word in input_sequence])
            y.append(word_to_index[output_word])

    return X, y

# Load the data
#tokenized_sentences, word_to_index, index_to_word = load_data('data/cleaned_files/reddit_casual.txt')
tokenized_sentences, word_to_index, index_to_word = load_data('data/cleaned_files/test_data.txt')
max_len_sentence = max(len(sentence) for sentence in tokenized_sentences)
for sentence in tokenized_sentences:
    sentence = list(mit.padded(sentence, '<PAD>', max_len_sentence))
print(tokenized_sentences)
X_train, y_train = create_training_data(tokenized_sentences, word_to_index, max_len_sentence)
