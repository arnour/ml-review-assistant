from ml_text_assistant.preparation import Preparator
from . import TestBase


class PreparationTestCase(TestBase):

    def setUp(self):
        self.preparator = Preparator()
        self.text = """
        ABSTRACT 
        Background.  Testing  is  an  essential  activity  in  the  software.
        In ESEM' 20: ACM/IEEE International!
        Write some tests. I love tests.
        """

    def test_prepare_tokens(self):
        tokens = self.preparator.prepare(self.text, stem=True, unique=True)
        expected = ['write',
                    'background',
                    'activ',
                    'abstract',
                    'softwar',
                    'esem',
                    'acmiee',
                    'essenti',
                    'intern',
                    'test',
                    'love'
                    ]

        self.assertEqual(tokens, set(expected))

    def test_prepare_tokens_not_stemmed_with_repetitions(self):
        tokens = self.preparator.prepare(self.text, stem=False, unique=False)
        expected = ['abstract',
                    'background',
                    'testing',
                    'essential',
                    'activity',
                    'software',
                    'esem',
                    'acmieee',
                    'international',
                    'write',
                    'tests',
                    'love',
                    'tests']

        self.assertEqual(tokens, expected)

    def test_tokens_should_be_lower_case(self):
        tokens = self.preparator.prepare(self.text)

        self.assertIn("abstract", tokens)
        self.assertIn("testing", tokens)

    def test_tokens_should_remove_non_alphabetical(self):
        tokens = self.preparator.prepare(self.text)

        self.assertNotIn("20", tokens)
        self.assertNotIn("'", tokens)

    def test_tokens_should_remove_ponctuation(self):
        tokens = self.preparator.prepare(self.text)

        self.assertNotIn(".", tokens)
        self.assertNotIn(":", tokens)
        self.assertNotIn("/", tokens)

    def test_tokens_should_remove_stopwords(self):
        tokens = self.preparator.prepare(self.text)

        self.assertNotIn("is", tokens)
        self.assertNotIn("an", tokens)
        self.assertNotIn("in", tokens)
        self.assertNotIn("the", tokens)

    def test_tokens_should_be_stemmed(self):
        tokens = self.preparator.prepare(self.text, stem=True)

        self.assertIn("test", tokens)
        self.assertNotIn("testing", tokens)

    def test_tokens_should_contain_only_unique_terms(self):
        tokens = self.preparator.prepare(self.text, unique=True)

        self.assertEqual(type(set()), type(tokens))
