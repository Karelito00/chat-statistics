from core.lang_recognition import Tokenizer, Recognizer

class TestRecognizer():
    sentences = [
        "My name is Scarlett Johansson. I'm very good.",
        "Mira lo que está cocinando papá",
        "Mi prude il culo",
    ]
    results = [
        "english",
        "spanish",
        "italian"
    ]

    def test_instance_recognizer(self):
        """
        Should tokenize creating an instance of the Recognizer class
        and calling tokenize giving text by parameter
        """
        for it, sentence in enumerate(self.sentences):
            tokens = Tokenizer().tokenize(sentence)
            recognizer = Recognizer()
            assert recognizer.recognize(tokens).best_lang == self.results[it]

    def test_instance_tokenizer_with_params(self):
        """
        Should tokenize creating an instance of the Tokenizer class
        with text as parameter and call tokenize without params
        """
        for it, sentence in enumerate(self.sentences):
            tokens = Tokenizer().tokenize(sentence)
            recognizer = Recognizer(tokens)
            assert recognizer.recognize().best_lang == self.results[it]

    def test_call_tokenizer(self):
        """
        Should tokenize calling directly the Tokenizer instance
        without being previously instanciated
        """
        for it, sentence in enumerate(self.sentences):
            tokens = Tokenizer().tokenize(sentence)
            
            assert Recognizer()(tokens).best_lang == self.results[it]
            assert Recognizer(tokens)().best_lang == self.results[it]
