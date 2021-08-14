from nltk import wordpunct_tokenize
from nltk.corpus import stopwords


class Tokenizer:
    def __init__(self, text=None):
        self.text = text

    def __call__(self, text=None):
        return self.tokenize(text if text else self.text)

    def tokenize(self, text=None):
        text_to_tokenize = self.text if text is None else text
        return wordpunct_tokenize(text_to_tokenize)


class Recognizer:
    class RecognizerResponse:
        def __init__(self, best_lang, best_ratio, lang_ratios):
            self.best_ratio = best_ratio
            self.best_lang = best_lang
            self.lang_ratios = lang_ratios

    def __init__(self, tokens=None):
        self.tokens = tokens

    def __call__(self, tokens=None):
        return self.recognize(tokens if tokens else self.tokens)

    def recognize(self, tokens=None):
        tokens = self.tokens if tokens is None else tokens
        tokens = [word.lower() for word in tokens]

        best_lang, best_ratio = None, 0
        lang_ratios = dict()

        for lang in stopwords.fileids():
            stopwords_set = set(stopwords.words(lang))
            words_set = set(tokens)
            common_elements = words_set.intersection(stopwords_set)
            score = len(common_elements)
            lang_ratios[lang] = score # Score function

            if best_lang is None or score > best_ratio:
                best_lang, best_ratio = lang, score

        return self.RecognizerResponse(best_lang, best_ratio, lang_ratios)
