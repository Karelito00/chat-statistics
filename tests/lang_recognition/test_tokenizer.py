from core.lang_recognition import Tokenizer

class TestTokenizer():
    sentence = "My name is Scarlett Johansson. I'm very good."
    result = ["My", "name", "is", "Scarlett", "Johansson", ".", "I", "'", "m", "very", "good", "."]

    def test_instance_tokenizer(self):
        """
        Should tokenize creating an instance of the Tokenizer class
        and calling tokenize giving text by parameter
        """
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(self.sentence)
        assert tokens == self.result

    def test_instance_tokenizer_with_params(self):
        """
        Should tokenize creating an instance of the Tokenizer class
        with text as parameter and call tokenize without params
        """
        tokenizer = Tokenizer(self.sentence)
        tokens = tokenizer.tokenize()
        assert tokens == self.result

    def test_call_tokenizer(self):
        """
        Should tokenize calling directly the Tokenizer instance
        without being previously instanciated
        """
        assert Tokenizer()(self.sentence) == self.result
        assert Tokenizer(self.sentence)() == self.result
