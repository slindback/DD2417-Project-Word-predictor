from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset
import torch.nn as nn
import argparse
import torch
import sys
import os

class RNNWordPredictor(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNNWordPredictor, self).__init__()
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.rnn = nn.GRU(hidden_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        embedded = self.embedding(x)
        output, _ = self.rnn(embedded)
        output = self.fc(output[:, -1, :])  # Predict the last word in the sequence
        return output


class WordPredictionDataset(Dataset):
    def __init__(self, sequences):
        self.sequences = sequences

    def __getitem__(self, index):
        return self.sequences[index]

    def __len__(self):
        return len(self.sequences)


def main(input_sentence,file,destination,epochs):
    # Define the command-line arguments parser
    """
    parser = argparse.ArgumentParser(description='RNN')
    parser.add_argument('--file', '-f', type=str, required=True, help='file used to train language model')
    parser.add_argument('--destination', '-d', type=str, help='file in which to store the language model')
    parser.add_argument('--epochs', '-e', type=int, default=1, help='number of epochs for training')
    """

    # Access the command-line arguments
    """arguments = parser.parse_args(sys.argv[1:])"""

    # Check if the model file exists
    """model_path = arguments.destination"""
    model_path = destination
    if os.path.exists(model_path):
        # Load the existing vocabulary and model
        dir = os.path.dirname(model_path)
        word_to_index = torch.load(dir+'/vocabulary.pt')

        input_size = len(word_to_index)
        hidden_size = 64
        output_size = input_size

        model = RNNWordPredictor(input_size, hidden_size, output_size)
        model.load_state_dict(torch.load(model_path))
    else:
        # Preprocessing
        """with open(arguments.file, 'r', encoding='utf8') as file:"""
        with open(file, 'r', encoding='utf8') as file:
            lines = file.readlines()
            sentences = [line.strip().lower().split() for line in lines]

        max_len_sentence = maxLength = max(len(sentence) for sentence in sentences)
        sentences = [sentence+["<PAD>"]*(max_len_sentence-len(sentence)) for sentence in sentences]

        word_to_index = {'<PAD>': 0}  # Padding symbol is mapped to index 0
        for sentence in sentences:
            for word in sentence:
                if word not in word_to_index:
                    word_to_index[word] = len(word_to_index)

        # Saving vocabulary to file
        dir = os.path.dirname(model_path)
        torch.sace(word_to_index, dir+'/vocabulary.pt')

        # Convert words to indices
        numerical_sentences = [[word_to_index[word] for word in sentence] for sentence in sentences]

        # Pad sequences
        padded_sentences = pad_sequence([torch.tensor(sentence) for sentence in numerical_sentences], batch_first=True)

        # Training
        input_size = len(word_to_index)
        hidden_size = 64
        output_size = input_size

        # Create a new model and train it
        model = RNNWordPredictor(input_size, hidden_size, output_size)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        # Create a DataLoader for efficient batching
        dataset = WordPredictionDataset(padded_sentences)
        dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

        # Training loop
        """num_epochs = arguments.epochs"""
        num_epochs = epochs
        for epoch in range(num_epochs):
            for batch in dataloader:
                optimizer.zero_grad()
                input_batch = batch[:, :-1]  # Input: n words
                target_batch = batch[:, 1:].flatten()  # Output: (n+1)th word prediction

                # Exclude padding elements from the input and target tensors
                input_sequences = [input_seq[input_seq != word_to_index['<PAD>']] for input_seq in input_batch]
                target_sequences = [target_seq[target_seq != word_to_index['<PAD>']] for target_seq in target_batch]

                total_loss = 0
                num_sequences = len(input_sequences)
                for i in range(num_sequences):
                    input_seq = input_sequences[i].unsqueeze(0)
                    target_seq = target_sequences[i].unsqueeze(0)

                    # Check if the input or target sequence length is 0
                    if input_seq.numel() == 0 or target_seq.numel() == 0:
                        continue  # Skip empty input or target sequences

                    output = model(input_seq)
                    output = output.squeeze(0)
                    target_seq = target_seq.squeeze()

                    loss = criterion(output, target_seq)
                    total_loss += loss

                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                if num_sequences > 0:
                    total_loss /= num_sequences

        # Save the trained model
        torch.save(model.state_dict(), model_path)

    # Generating predictions
    def predict_next_words(input_sentence, model, word_to_index, top_k=3):
        model.eval()
        numerical_input = torch.tensor([word_to_index.get(word, 0) for word in input_sentence]).unsqueeze(0)
        output = model(numerical_input)
        _, top_indices = torch.topk(output, k=top_k, dim=1)
        predicted_words = [list(word_to_index.keys())[list(word_to_index.values()).index(idx.item())] for idx in top_indices[0]]
        return predicted_words

    predicted_words = predict_next_words(input_sentence, model, word_to_index, top_k=3)
    return predicted_words


if __name__ == '__main__':
    input_sentence = ["this", "is", "why"]  # Default input sentence
    predicted_words = main(input_sentence)
    print("Predicted next words:", predicted_words)
