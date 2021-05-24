import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer


class Preparator:
    """Prepare corpus for text"""

    def __init__(self, download=False):
        if download:
            nltk.download("punkt")
            nltk.download("stopwords")

    def prepare(self, text, stem=False, unique=False):
        words = word_tokenize(text)
        operations = [
            self.__case_normalizer,
            self.__remove_ponctuation,
            self.__remove_non_alphabetic,
            self.__remove_stopwords
        ]

        if stem:
            operations = operations + [self.__stem_words]

        if unique:
            operations = operations + [self.__unique]

        for op in operations:
            words = op(words)
        return words

    def __case_normalizer(self, words):
        return [w.lower() for w in words]

    def __remove_non_alphabetic(self, words):
        return [w for w in words if w.isalpha()]

    def __remove_ponctuation(self, words):
        table = str.maketrans('', '', string.punctuation)
        return [w.translate(table) for w in words]

    def __remove_stopwords(self, words):
        stop_words = set(stopwords.words('english'))
        return [w for w in words if w not in stop_words]

    def __stem_words(self, words):
        stemmer = EnglishStemmer()
        return [stemmer.stem(w) for w in words]

    def __unique(self, words):
        return set(words)
