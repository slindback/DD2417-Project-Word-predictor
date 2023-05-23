# Written by Simon Lindbäck and Anton Lewander
from Predictor import Predictor
import tkinter as tk
import string
VALID_KEYS = "qwertyuiopasdfghjklzxcvbnm"

class Display:
    def __init__(self, root):
        #self.predictor = Predictor("data/models/Purdue_Calumet_text_Message_Corpus_model.txt")
        #self.predictor = Predictor("data/models/smsCorpus_en_model.txt")
        self.predictor = Predictor("data/models/reddit_casual_model.txt")
        self.predictor.read_model()
        self.strokes_saved = 0

        self.root = root
        self.root.title("Text Conversation")

        self.strokes_label = tk.Label(self.root, text="Strokes saved: 0")
        self.strokes_label.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=(10, 0))

        self.conversation_text = tk.Text(self.root, height=8, width=40)  # Decrease the height value here
        self.conversation_text.pack(side=tk.TOP, padx=10, pady=10)

        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(side=tk.TOP, padx=10, pady=10)
        self.entry.bind("<KeyRelease>", self.handle_update)
        self.entry.bind("<Return>", self.send_message)

        self.suggestion_frame = tk.Frame(self.root)
        self.suggestion_frame.pack(side=tk.TOP)

        self.suggestion_labels = []
        self.suggestions = []

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.TOP, padx=10, pady=10)


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
        for i in range(3):
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
        self.entry.insert(tk.END, suggestion+' ')
        self.strokes_saved += len(suggestion)
        self.strokes_label.config(text=f"Strokes saved: {self.strokes_saved}")
        self.handle_update(None)

    def handle_update(self, event):
        if event is None or event.keysym.lower() in VALID_KEYS:
            self.extract_last_word()
            self.predict_current_word()
        self.check_space()

    def check_space(self):
        current_text = self.entry.get()
        if current_text.endswith(' '):
            # Perform the desired action when a new space is entered
            word = self.extract_last_word()
            self.generate_predictions(word)

    def predict_current_word(self):
        word = self.extract_last_word()
        try:
            self.suggestions = self.predictor.predict_current(word)
            if self.suggestions != []:
                self.display_suggestions()
        except: pass

    def generate_predictions(self, word):
        try:
            self.suggestions = self.predictor.predict(word)
            if self.suggestions != []:
                self.display_suggestions()
        except: pass

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
