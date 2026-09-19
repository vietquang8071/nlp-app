import pandas as pd
import numpy as np
import re
from collections import Counter

class MyTfIdfVectorizer():
  def __init__(self, data:pd.DataFrame, tokenizer=None):
    self.data = data
    self._custom_tokenizer = tokenizer

    self.vocab = None
    self.word_to_idx = None

    self.count_matrix = None
    self.tf = None
    self.df = None
    self.idf = None
    self.tfidf = None
    self.cosine_similarity = None

  def _default_tokenize(self, text: str):
    """Default tokenizer: normalize then split by whitespace."""
    return self._normalization(text).split()

  def _tokenize(self, text: str):
    """Tokenize text using custom tokenizer if provided, otherwise default."""
    if self._custom_tokenizer is not None:
      return self._custom_tokenizer(text)
    return self._default_tokenize(text)

  def buildVocabulary(self, col_name:str):
    vocabulary = set()

    for text in self.data[col_name]:
      tokens = self._tokenize(text)
      vocabulary.update(tokens)

    self.vocab = sorted(vocabulary)
    self.word_to_idx = {
      word: idx for idx, word in enumerate(self.vocab)
    }

  def _normalization(self, text: str):
    return re.sub(r'[^\w\s]', '', text).lower()

  def _compute_counts_for_each_text(self, text: str):
    tokens = self._tokenize(text)
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

  def transform_query(self, query: str):
    """Transform a raw query string into a L2-normalized TF-IDF vector
    using the existing vocabulary and IDF weights."""
    tokens = self._tokenize(query)
    query_counts = np.zeros(len(self.vocab), dtype=np.float64)
    counts = Counter(tokens)
    for token, count in counts.items():
      if token in self.word_to_idx:
        idx = self.word_to_idx[token]
        query_counts[idx] = count
    query_tf = query_counts
    query_tfidf = query_tf * self.idf
    norm = np.linalg.norm(query_tfidf)
    if norm > 0:
      query_tfidf = query_tfidf / norm

    return query_tfidf

  def search(self, query: str, top_k: int = 5, preview_len: int = 200):
    query_vector = self.transform_query(query)
    similarities = self.tfidf @ query_vector
    top_k_indices = np.argsort(similarities)[::-1][:top_k]

    col_name = [col for col in self.data.columns if self.data[col].dtype == object][0]

    results = pd.DataFrame({
      'Rank': range(1, top_k + 1),
      'Document ID': top_k_indices,
      'Similarity': [f"{similarities[i]:.4f}" for i in top_k_indices],
      'Document Preview': [
        self.data[col_name].iloc[i][:preview_len] + "..."
        for i in top_k_indices
      ]
    })

    return results
