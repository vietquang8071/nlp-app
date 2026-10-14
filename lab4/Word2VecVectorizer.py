import os
import re
import numpy as np
from gensim.models import Word2Vec
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

class Word2VecVectorizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        vector_size=300,
        window=5,
        min_count=2,
        epochs=10,
        workers=os.cpu_count() or 4,
    ):
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
        self.epochs = epochs
        self.workers = workers
        

    def _tokenize(self, text):
        clean_str = re.sub(r"<.*?>", " ", str(text).lower())
        return re.findall(r"\b[a-zA-Z]+\b", clean_str)

    def fit(self, X, y=None):
        sentences = [self._tokenize(text) for text in X]
        self.w2v_ = Word2Vec(
            sentences=sentences,
            vector_size=self.vector_size,
            window=self.window,
            min_count=self.min_count,
            workers=self.workers,
            seed=42,
            epochs=self.epochs
        )
        return self

    def transform(self, X):
        check_is_fitted(self, "w2v_")
        vectors = []
        for text in X:
            tokens = self._tokenize(text)
            word_vectors = [
                self.w2v_.wv[word]
                for word in tokens
                if word in self.w2v_.wv
            ]
            if word_vectors:
                doc_vector = np.mean(word_vectors, axis=0)
            else:
                doc_vector = np.zeros(self.vector_size)
            vectors.append(doc_vector)
        return np.array(vectors)