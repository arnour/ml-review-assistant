from gensim.corpora.dictionary import Dictionary
from gensim.models.coherencemodel import CoherenceModel
from operator import itemgetter
from collections import Counter
import numpy as np


class Explorer:
    """Expose topic modeling metrics"""

    def __init__(self, tokens):
        self.__tokens = tokens
        self.__dictionary = Dictionary(tokens)
        self.__corpus = [self.__dictionary.doc2bow(token) for token in tokens]
        self.__scores = []
        flatten_tokens = [item for sublist in tokens for item in sublist]
        self.__top = Counter(flatten_tokens).most_common(100)

    def scores(self):
        return self.__scores.copy()

    def top(self):
        return self.__top.copy()

    def best(self):
        return sorted(self.__scores, key=itemgetter(1), reverse=True)[0][0]

    def coherence(self, topics, model_builder, measure='u_mass'):
        cm = CoherenceModel(
            model=model_builder(topics, self.__corpus, self.__dictionary),
            corpus=self.__corpus,
            texts=self.__tokens,
            dictionary=self.__dictionary,
            coherence=measure
        )
        self.__scores.append((topics, round(cm.get_coherence(), 5)))

    def resume(self, topics, model_builder):
        model = model_builder(topics, self.__corpus, self.__dictionary)
        topics_resume = []
        for topic_id, weighted in model.show_topics(formatted=False):
            keywords = [word for word, _ in weighted]
            topics_resume.append(keywords)
        res = []
        for token_index, row in enumerate(model[self.__corpus]):
            row = sorted(row, key=itemgetter(1), reverse=True)
            (topic_id, topic_score) = row[0]
            res.append(
                np.array(
                    [
                        int(topic_id),
                        round(topic_score, 5),
                        topics_resume[topic_id],
                        token_index
                    ],
                    dtype=object
                )
            )
        return res
