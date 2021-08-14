"""
Module for Language recognition using nltk
"""
from .main import (
  Tokenizer,
  Recognizer
)


class MethodNotFound(Exception):
    pass


def recognize(text: str, method="stopwords") -> Recognizer.RecognizerResponse:
    """
    Recognize language using the method specified
    
    text: The text to be processed
    method: The method for detect language -> ["stopwords"]

    Example:
    >>> result = recognize("My name is Scarlett Johansson. I'm very good.")
    >>> print(result.best_lang) # english
    >>> print(result.best_ratio) # 5
    >>> print(result.lang_ratios) # dict({'english': 5, ...})
    """
    if method == "stopwords":
        tokenizer = Tokenizer()
        tokens = tokenizer(text)
        return Recognizer().recognize(tokens)
    else:
        raise MethodNotFound("Method not found")
