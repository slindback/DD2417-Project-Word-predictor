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
    def __init__(self, path):
        self.model_path = path
        self.i2w = {}
        self.w2i = {}
        self.unigram_count = defaultdict(int)
        self.bigram_count = defaultdict(lambda: defaultdict(int))
        self.bigram_prob = defaultdict(dict)
        self.unique_words = 0
        self.total_words = 0
        self.number_of_predictions = 3

    def read_model(self):
        try:
            with codecs.open(self.model_path, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))
                # YOUR CODE HERE
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
            print("Couldn't find bigram probabilities file {}".format(filename))
            return False

    """
    def predict_next_word(self, word, predictions=3):
        try:
            sample = self.bigram_prob[self.w2i[word]]
            most_probable = heapq.nsmallest(predictions, sample, key=lambda k: abs(sample[k]))
            return [self.i2w[ind] for ind in most_probable]
        except:
            return []
    """

    def predict(self, w):
        """
        Generates and prints n predictions by sampling from the distribution of the language model.
        """
        w=w.lower()
        predictions = []

        for word in range(self.number_of_predictions):
            try:
                if self.w2i[w] in self.bigram_prob:
                    distr = {key: math.exp(value) for key, value in self.bigram_prob[self.w2i[w]].items()}
                    outcomes, weights = zip(*distr.items())
                    prediction = self.i2w[random.choices(outcomes, weights=weights)[0]]

                else: prediction = random.choice(list(self.i2w.values()))

                if prediction not in predictions: predictions.append(prediction)
            except: pass
        return predictions

    def predict_current(self, w):
        w=w.lower()
        predictions = []
        words = [i for i in list(self.w2i.keys()) if w in i and i.startswith(w)]
        for word in range(self.number_of_predictions):
            try:
                prediction = random.choice(words)

                if prediction not in predictions: predictions.append(prediction)
            except: pass
        return predictions

def main():
    """
    Parse command line arguments
    """



    """
    TAKES WORD THROUGH COMMAND LINE AND PRINTS PREDICTIONS
    ------------------------------------------------------------------------
    """

    """
    parser = argparse.ArgumentParser(description='BigramTester')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file with language model')
    parser.add_argument('--word', '-w', type=str, required=True, help='word')
    parser.add_argument('--number_of_predictions', '-n', type=int, default=3)

    arguments = parser.parse_args()

    predictor = Predictor(arguments.file)
    predictor.read_model()
    predictions = predictor.predict(arguments.word,arguments.number_of_predictions)
    print(predictions)
    """



    """
    COMPARISON OF THE THREE DATAMODELS - PRINTS STROKES SAVED IN PERCENTAGES
    ------------------------------------------------------------------------
    """
    models =    ["data/models/Purdue_Calumet_text_Message_Corpus_model.txt",
                 "data/models/smsCorpus_en_model.txt",
                 "data/models/reddit_casual_model.txt"]

    sentencesx = [   "hey hows it going",
                    "just wanted to say hi and see how your day is going",
                    "i cant wait to catch up with you its been too long",
                    "guess what i just found out i won two tickets to the concert",
                    "im so excited for the weekend any plans",
                    "i heard theres a new coffee shop in town wanna check it out together",
                    "remember that time we went hiking it was such a great adventure",
                    "im craving pizza do you want to order some for dinner",
                    "i cant stop listening to this new song you should give it a listen too",
                    "have you watched the latest episode of our favorite tv show its mindblowing",
                    "im thinking of redecorating my room any suggestions",
                    "did you hear about the new job opening i think youd be a perfect fit",
                    "i cant believe its already may time flies",
                    "have you seen the latest movie everyones talking about lets go watch it together",
                    "i just finished reading an amazing book i think youd love it too",
                    "do you want to join me for a workout session at the gym",
                    "im feeling adventurous lets plan a road trip",
                    "i have a surprise for you cant wait to see your reaction",
                    "im having a lazy sunday want to join me for a movie marathon",
                    "i cant believe how beautiful the sunset is today wish you were here to enjoy it too",
                    "im trying out a new recipe tonight fingers crossed it turns out delicious",
                    "hey remember that inside joke we have it still cracks me up",
                    "i just finished a painting id love to hear your thoughts on it",
                    "i found an old photo album it brought back so many memories",
                    "im attending a concert next week you should come with me",
                    "im feeling a bit stressed any tips on how to relax",
                    "i cant wait for summer vacation its going to be epic",
                    "have you tried that new restaurant in town the food is amazing",
                    "im going to a book signing event do you want me to get you an autograph too",
                    "i just adopted a new pet its the cutest thing ever",
                    "im going to a costume party any ideas on what i should dress up as",
                    "im learning a new language its challenging but exciting",
                    "remember that time we danced in the rain it was so much fun",
                    "im planning a surprise party can you help me with the preparations",
                    "im going on a weekend getaway can you recommend a great destination",
                    "i just watched a documentary that changed my perspective on life mind blown",
                    "im attending a photography workshop ill share the photos with you later",
                    "i just finished a puzzle it was harder than i expected",
                    "im starting a new hobby cant wait to show you what i create",
                    "im organizing a movie night which genre should we go for",
                    "im going to a music festival lets dance our hearts out",
                    "i just discovered a new hiking trail we should explore it together",
                    "im planning a picnic in the park want to join me",
                    "im attending a yoga retreat ill come back all zen and relaxed",
                    "hey hows it going",
                    "just wanted to say hi",
                    "thinking of you",
                    "hope youre having a great day",
                    "wanna grab a coffee sometime",
                    "cant wait to see you",
                    "remember our fun times together",
                    "lets meet up soon",
                    "how are you doing",
                    "sending good vibes your way",
                    "miss hanging out with you",
                    "lets go on an adventure",
                    "hope you have a wonderful day",
                    "whats new with you",
                    "thinking about our laughter",
                    "lets plan a get-together",
                    "hope everything is going well",
                    "sending love and hugs",
                    "miss our late-night chats",
                    "lets catch up over lunch",
                    "how's life treating you",
                    "thinking of the good times",
                    "lets have a movie marathon",
                    "hope your day is filled with joy",
                    "whats your favorite song",
                    "missing your company",
                    "lets plan a road trip",
                    "hope you're smiling today",
                    "sending positive energy your way",
                    "remember our silly moments",
                    "lets grab dinner soon",
                    "how's the weather there",
                    "thinking of the memories we've made",
                    "lets have a game night",
                    "hope you're enjoying the little things",
                    "whats your favorite book",
                    "missing our inside jokes",
                    "lets plan a picnic in the park",
                    "hope we can meet up soon",
                    "sending you positive vibes",
                    "remember when we danced in the rain",
                    "lets have a coffee date",
                    "how's your day going so far",
                    "thinking of you and smiling",
                    "hope you're surrounded by happiness",
                    "whats your favorite movie",
                    "missing your laughter",
                    "lets go for a hike this weekend",
                    "hope you're taking care of yourself",
                    "sending you good thoughts",
                    "remember our adventure last summer",
                    "lets plan a weekend getaway",
                    "how's work treating you",
                    "thinking of the fun times we've had",
                    "hope you're having a fantastic day",
                    "whats your favorite food",
                    "missing our long conversations",
                    "lets explore a new place together",
                    "hope we can catch up soon",
                    "sending positive vibes your way",
                    "remember our karaoke night",
                    "lets have a beach day",
                    "how's your family doing",
                    "thinking of you always",
                    "hope you're enjoying the sunshine",
                    "whats your favorite hobby",
                    "missing our hangouts",
                    "lets go for a walk in the park",
                    "hope you're doing amazing",
                    "sending you warm wishes",
                    "remember when we stargazed",
                    "lets meet for brunch"
                ]
    sentences = ["hello how are you"]
    total_chars = 0
    for sentence in sentences:
        sentence = sentence.split()
        total_chars += len(sentence)

    for model in models:
        generator = Predictor(model)
        generator.read_model()
        strokes_saved = 0
        for sentence in sentences:
            sentence = sentence.split()
            for i in range(len(sentence)):
                predictions = generator.predict(sentence[i])
                if i+1 in range(len(sentence)):
                    if sentence[i+1] in predictions:
                        strokes_saved += len(sentence[i+1])
        percentage = str(round((strokes_saved/total_chars) * 100))
        print("{} keystrokes saved with {}. Percentage: {}%".format(strokes_saved, os.path.basename(model), percentage))

if __name__ == "__main__":
    main()
