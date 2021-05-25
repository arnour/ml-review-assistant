from . import TestBase
from ml_review_assistant.exploration import Explorer
from gensim.models.nmf import Nmf
from gensim.test.utils import common_texts
import numpy as np


class ExplorationTestCase(TestBase):

    def setUp(self):
        self.tokens = common_texts
        self.explorer = Explorer(tokens=self.tokens)

    def test_generate_coherence_score_for_each_model(self):
        for topics in range(5, 20, 5):
            self.explorer.coherence(topics, self.__model_builder)

        scores = self.explorer.scores()

        self.assertEqual(len(scores), 3)
        self.assertEqual(scores[0][0], 5)
        self.assertIsNotNone(scores[0][1])

        self.assertEqual(scores[1][0], 10)
        self.assertIsNotNone(scores[0][1])

        self.assertEqual(scores[2][0], 15)
        self.assertIsNotNone(scores[0][1])

    def test_select_best_number_of_topics(self):
        for topics in range(1, 4):
            self.explorer.coherence(topics, self.__model_builder)

        self.assertEqual(self.explorer.best(), 2)

    def test_select_top_tokens(self):
        expected_top = [('system', 4),
                        ('user', 3),
                        ('trees', 3),
                        ('graph', 3),
                        ('human', 2),
                        ('interface', 2),
                        ('computer', 2),
                        ('survey', 2),
                        ('response', 2),
                        ('time', 2),
                        ('eps', 2),
                        ('minors', 2)]

        self.assertEqual(self.explorer.top(), expected_top)

    def test_resume_topics(self):
        result = self.explorer.resume(2, self.__model_builder)
        topic0_keywords = [
            'system', 'eps', 'user', 'human', 'interface',
            'response', 'time', 'graph', 'computer', 'trees'
        ]
        topic1_keywords = [
            'survey', 'computer', 'time', 'response', 'user',
            'graph', 'minors', 'trees', 'system', 'interface'
        ]

        expected = [
            np.array([1, 0.75065, topic1_keywords, 0], dtype='object'),
            np.array([1, 0.84832, topic1_keywords, 1], dtype='object'),
            np.array([0, 1.0, topic0_keywords, 2], dtype='object'),
            np.array([0, 1.0, topic0_keywords, 3], dtype='object'),
            np.array([1, 0.91701, topic1_keywords, 4], dtype='object'),
            np.array([1, 1.0, topic1_keywords, 5], dtype='object'),
            np.array([1, 1.0, topic1_keywords, 6], dtype='object'),
            np.array([1, 1.0, topic1_keywords, 7], dtype='object'),
            np.array([1, 1.0, topic1_keywords, 8], dtype='object'),
        ]

        for r, e in zip(result, expected):
            self.assertEqual(r[0], e[0])
            self.assertAlmostEqual(r[1], e[1])
            self.assertEqual(r[2], e[2])
            self.assertEqual(r[3], e[3])

    def __model_builder(self, t, c, d):
        return Nmf(
            corpus=c,
            id2word=d,
            num_topics=t,
            random_state=42,
        )
