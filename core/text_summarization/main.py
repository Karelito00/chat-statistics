import nltk
import string
from heapq import nlargest

class Text_Summarization:

    def __init__(self, messages, language = "spanish"):
        self.messages = messages
        self.language = language

    def remove_punctuation(self, texts):
        new_texts = []
        for text in texts:
            n_text = ""
            for c in text:
                n_text += "" if c in string.punctuation else c
            new_texts.append(n_text)
        return new_texts

    def remove_stopwords(self, texts):
        new_texts = []
        for text in texts:
            n_text = [word for word in text.split() if word.lower() not in nltk.corpus.stopwords.words(self.language)]
            new_texts.append(" ".join(n_text))
        return new_texts

    def remove_numbers(self, texts):
        new_texts = []
        for text in texts:
            n_text = ""
            for c in text:
                n_text += "" if c.isdigit() else c
            new_texts.append(n_text)
        return new_texts


    def calculate_normalized_frequency(self, texts):
        new_texts = []
        for text in texts:
            word_freq = {}
            words = text.split(' ')

            for word in words:
                if word not in word_freq:
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1

            max_word_freq = max(word_freq.values())
            for word in word_freq.keys():
                word_freq[word] = word_freq[word] / max_word_freq

            summary_words = nlargest(20, word_freq, key=word_freq.get)
            new_texts.append(" ".join(summary_words))

        return new_texts

    def run(self):
        new_messages = self.remove_punctuation(self.messages)
        new_messages = self.remove_stopwords(new_messages)
        new_messages = self.remove_numbers(new_messages)
        new_messages = self.calculate_normalized_frequency(new_messages)
        return [message.lower() for message in new_messages]
