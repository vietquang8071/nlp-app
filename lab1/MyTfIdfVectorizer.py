import pandas as pd
import numpy as np
import re
from collections import Counter

class MyTfIdfVectorizer():
  def __init__(self, data:pd.DataFrame):
    self.data = data

    self.vocab = None
    self.word_to_idx = None

    self.count_matrix = None
    self.tf = None
    self.df = None
    self.idf = None
    self.tfidf = None
    self.cosine_similarity = None

  def buildVocabulary(self, col_name:str):
    vocabulary = set()

    for text in self.data[col_name]:
      tokens = self._normalization(text).split()
      vocabulary.update(tokens)

    self.vocab = sorted(vocabulary)
    self.word_to_idx = {
      word: idx for idx, word in enumerate(self.vocab)
    }

  def _normalization(self, text: str):
    return re.sub(r'[^\w\s]', '', text).lower()

  def _compute_counts_for_each_text(self, text: str):
    normalized_text = self._normalization(text)
    tokens = normalized_text.split()
    vector = np.zeros((len(self.vocab)), dtype=np.float32)

    counts = Counter(tokens)
    for token, count in counts.items():
      idx = self.word_to_idx[token]
      vector[idx] = count
    return vector
  
  def compute_counts(self, col_name: str):
    vectors = []
    for text in self.data[col_name]:
      vector = self._compute_counts_for_each_text(text)
      vectors.append(vector)
    self.count_matrix = np.array(vectors)

  def compute_tf(self):
    self.tf = self.count_matrix.astype(np.float64)

  def compute_df(self):
    binary_matrix = self.count_matrix > 0
    self.df = np.sum(binary_matrix, axis=0)

  def compute_idf(self):
    num_doc = self.count_matrix.shape[0]
    self.idf = np.log((1 + num_doc) / (1 + self.df)) + 1

  def compute_tfidf(self):
    weighted_tfidf = self.tf * self.idf

    norms = np.linalg.norm(
        weighted_tfidf,
        axis=1,
        keepdims=True
    )

    self.tfidf = np.divide(
        weighted_tfidf,
        norms,
        out=np.zeros_like(weighted_tfidf),
        where=norms != 0
    )

  def compute_cosine_similarity(self):
    dot_product = self.tfidf @ self.tfidf.T
    norms = np.linalg.norm(self.tfidf, axis=1, keepdims=True)

    self.cosine_similarity = np.divide(
      dot_product,
      norms @ norms.T,
      out=np.zeros_like(dot_product),
      where=norms @ norms.T != 0
    )

    return self.cosine_similarity

