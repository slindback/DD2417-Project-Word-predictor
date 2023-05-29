# Written by Simon Lindbäck and Anton Lewander
from RNN import main as rnn_main
from Predictor import Predictor
import tkinter as tk
import string
import os
VALID_KEYS = "qwertyuiopasdfghjklzxcvbnm"

class Display:
    def __init__(self, root):
        self.predictor = Predictor("data/Bigram_models/reddit_casual_model.txt")
        self.predictor.read_model()
        self.strokes_saved = 0

        self.root = root
        self.root.title("Text Conversation")

        self.strokes_label = tk.Label(self.root, text="Strokes saved: 0")
        self.strokes_label.grid(row=0, column=1, sticky=tk.NE, padx=10, pady=(10, 0))

        # Create the toggle button
        self.toggle_button = tk.Button(self.root, text="RNN", command=self.toggle_mode)
        self.toggle_button.grid(row=0, column=0, sticky=tk.NW, padx=(10, 0), pady=10)

        # Set the initial mode
        self.RNN_enabled = True
        self.RNN_model_dir = os.path.dirname('data/RNN_models/reddit_casual/reddit_casual_model_e1.pth')

        self.conversation_text = tk.Text(self.root, height=8, width=40)  # Decrease the height value here
        self.conversation_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.entry = tk.Entry(self.root, width=40)
        self.entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.entry.bind("<KeyRelease>", self.handle_update)
        self.entry.bind("<Return>", self.send_message)

        self.suggestion_frame = tk.Frame(self.root)
        self.suggestion_frame.grid(row=3, column=0, columnspan=2)

        self.suggestion_labels = []
        self.suggestions = []

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


    def toggle_mode(self):
        if self.RNN_enabled:
            self.RNN_enabled = False
            self.toggle_button.config(text="Bigram")
        else:
            self.RNN_enabled = True
            self.toggle_button.config(text="RNN")

    def clean_word(self, word):
        clean_str = ""
        word = word.lower()
        for char in word:
            if not (char in string.punctuation or char in string.digits):
                clean_str += char
        return clean_str

    def display_suggestions(self):
        # Clear previous suggestions
        for label in self.suggestion_labels:
            label.destroy()
        self.suggestion_labels = []

        # Add new suggestions
        if self.suggestions != []:
            for i in range(len(self.suggestions)):
                label = tk.Label(self.suggestion_frame, text=self.suggestions[i], padx=5, pady=5)
                label.pack(side=tk.LEFT)
                self.suggestion_labels.append(label)
                label.bind("<Button-1>", lambda e, s=self.suggestions[i]: self.select_suggestion(s))

    def send_message(self, event=None):
        message = self.entry.get()
        self.conversation_text.insert(tk.END, f"You: {message}\n\n")
        self.entry.delete(0, tk.END)
        for label in self.suggestion_labels:
            label.destroy()
        self.conversation_text.see(tk.END)

    def select_suggestion(self, suggestion):
        if self.entry.get().endswith(' '):
            self.entry.insert(tk.END, ' '+suggestion+' ')
            self.strokes_saved += len(suggestion)
        else:
            self.strokes_saved += (len(suggestion)-len(self.extract_last_word()))
            self.entry.delete(len(self.entry.get())-len(self.extract_last_word()), tk.END)
            self.entry.insert(tk.END, suggestion)


        self.strokes_label.config(text=f"Strokes saved: {self.strokes_saved}")
        self.handle_update(None)

    def handle_update(self, event):
        if event is None or event.keysym.lower() in VALID_KEYS:
            self.predict_current_word()
        self.check_space()

    def check_space(self):
        current_text = self.entry.get()
        if current_text.endswith(' '):
            # Perform the desired action when a new space is entered
            word = self.extract_last_word()
            self.generate_predictions(word)

    def predict_current_word(self):
        word = self.extract_last_word().lower()
        self.suggestions = self.predictor.predict_current(word)
        if self.suggestions != []:
            self.display_suggestions()

    def toggle_mode(self):
        self.RNN_enabled = not self.RNN_enabled  # Toggle the RNN_enabled variable

        if self.RNN_enabled:
            self.toggle_button.config(text="RNN")
        else:
            self.toggle_button.config(text="Bigram")

    def generate_predictions(self, word):
        if self.RNN_enabled:
            # RNN model
            sentence = self.entry.get().split()
            self.suggestions = rnn_main(sentence, 'data/cleaned_files/reddit_casual.txt',
                                         'data/RNN_models/reddit_casual/reddit_casual_model_e1.pth', 1)
        else:
            # Bigram model
            try:
                self.suggestions = self.predictor.predict(word)
            except:
                self.suggestions = []

        self.display_suggestions()

    def extract_last_word(self):
        current_text = self.clean_word(self.entry.get())
        words = current_text.split()
        if len(words) > 0:
            return words[-1]

def main():
    root = tk.Tk()
    display = Display(root)
    root.mainloop()

if __name__ == "__main__":
    main()
