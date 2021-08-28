import pandas as pd
import nltk
import string
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier

# nltk.download('stopwords')
# nltk.download('wordnet')

class SpamDetection:
    def __init__(self):
        self.SPAM_STRINGS = ["@", '%', '£', '€', '\$', "T&C", "www|WWW", "http|HTTP", "https|HTTPS", "email|Email|EMAIL", "SMS|sms|FREEPHONE", ["\d{11}"], ["\d{10}"], ["\d{5}"]]

    def remove_punctuation_characters(self, text):
        n_text = ""
        for c in text:
            n_text += " " if c in string.punctuation or c.isdigit() else c
        return n_text

    #TODO: support for more languages, for now only spanish :(
    def remove_stopwords(self, text):
        result = []
        stopwords = nltk.corpus.stopwords.words('spanish')

        for word in text:
            if(word not in stopwords):
                result.append(word)

        return result


    def lemmatizer(self, text):
        result = []
        wordlem = nltk.WordNetLemmatizer()

        for word in text:
            result.append(wordlem.lemmatize(word))

        return result

    def train_model(self):
        train_data = pd.read_csv('./spam/spam.csv', encoding='latin-1')
        train_data = train_data[['v1', 'v2']]
        train_data.rename(columns={'v1': 'label', 'v2': 'text'}, inplace=True)
        train_data['label'] = [1 if text_type == "spam" else 0 for text_type in train_data['label']]
        train_data = train_data.drop_duplicates()
        train_data['length'] = train_data['text'].apply(len)
        train_data['contain'] = 0

        for spam_string in self.SPAM_STRINGS:
            if(type(spam_string) == list):
                train_data['contain'] = train_data['contain'] | train_data['text'].str.contains(spam_string[0], regex=True).map({False: 0, True: 1})
            else:
                train_data['contain'] = train_data['contain'] | train_data['text'].str.contains(spam_string).map({False: 0, True: 1})

        train_data['text'] = train_data['text'].apply(self.remove_punctuation_characters)
        train_data['token'] = [re.split("\W+", text.lower()) for text in train_data['text']]

        train_data['token'] = train_data['token'].apply(self.remove_stopwords)
        train_data['lem_text'] = train_data['token'].apply(self.lemmatizer)
        train_data.drop(['token'], axis = 1, inplace = True)

        train_data['final_text'] = [" ".join(text) for text in train_data["lem_text"]]
        train_data.drop(['lem_text', 'text'], axis = 1, inplace = True)

        y = train_data['label']
        x = train_data.drop(['label'], axis = 1)

        # It involves counting the number of occurrences of each word/token in a given text.
        # More on Count Vectorization: https://www.educative.io/edpresso/countvectorizer-in-python
        cv = CountVectorizer(max_features = 5000)
        self.bag_of_words_transformer = cv.fit(x['final_text'])
        self.message_bagofwords = self.bag_of_words_transformer.transform(x['final_text'])

        # It tells us how important a word is to a text in a group of text.
        # It is calculated by multiplying the frequency of a word, and
        # the inverse document frequency (how common a word is, calculated
        # by log(number of text/number of text which contains the word)) of
        # the word across a group of text.
        # More on TFIDF: https://monkeylearn.com/blog/what-is-tf-idf/
        tf = TfidfTransformer()
        self.tfidf_transformer = tf.fit(self.message_bagofwords)
        message_tfidf = self.tfidf_transformer.transform(self.message_bagofwords)
        self.model = RandomForestClassifier(n_estimators = 100, random_state = 0)
        self.model.fit(message_tfidf, y)


    def predict_text(self, text):
        bag_of_words_for_message = self.bag_of_words_transformer.transform([text])
        tfidf = self.tfidf_transformer.transform(bag_of_words_for_message)
        return self.model.predict((tfidf)[0][0])

    def predict_array(self, text_array):
        bag_of_words_for_message = self.bag_of_words_transformer.transform(text_array)
        tfidf = self.tfidf_transformer.transform(bag_of_words_for_message)
        return self.model.predict(tfidf)


