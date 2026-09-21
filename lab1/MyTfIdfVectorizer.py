import pandas as pd
import numpy as np
import re
from collections import Counter
from scipy import sparse

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

  def compute_counts(self, col_name: str):
    """Build a sparse CSR count matrix (docs × vocab)."""
    rows, cols, data = [], [], []

    for row_idx, text in enumerate(self.data[col_name]):
      tokens = self._tokenize(text)
      counts = Counter(tokens)
      for token, count in counts.items():
        if token in self.word_to_idx:
          rows.append(row_idx)
          cols.append(self.word_to_idx[token])
          data.append(count)

    n_docs = len(self.data)
    n_vocab = len(self.vocab)
    self.count_matrix = sparse.csr_matrix(
      (np.array(data, dtype=np.float64), (rows, cols)),
      shape=(n_docs, n_vocab)
    )

  def compute_tf(self):
    """TF = count / total words in document."""
    row_sums = np.asarray(self.count_matrix.sum(axis=1)).ravel()
    row_sums[row_sums == 0] = 1  # avoid division by zero
    inv_sums = sparse.diags(1.0 / row_sums)
    self.tf = (inv_sums @ self.count_matrix).tocsr()

  def compute_df(self):
    binary_matrix = (self.count_matrix > 0).astype(np.float32)
    self.df = np.asarray(binary_matrix.sum(axis=0)).ravel()

  def compute_idf(self):
    num_doc = self.count_matrix.shape[0]
    self.idf = np.log((1 + num_doc) / (1 + self.df)) + 1

  def compute_tfidf(self):
    # Multiply each row of tf by idf (element-wise broadcast)
    weighted_tfidf = self.tf.multiply(self.idf)

    # Compute L2 norm for each row
    norms = np.sqrt(
      np.asarray(
        weighted_tfidf.multiply(weighted_tfidf).sum(axis=1)
      ).ravel()
    )
    norms[norms == 0] = 1  # avoid division by zero

    # Normalize: multiply each row by 1/norm using a diagonal matrix
    inv_norms = sparse.diags(1.0 / norms)
    self.tfidf = (inv_norms @ weighted_tfidf).tocsr()

  def compute_cosine_similarity(self):
    """Compute doc-to-doc cosine similarity.
    WARNING: Creates a dense (n_docs × n_docs) matrix.
    Only use this on small corpora (Part E)."""
    # tfidf is already L2-normalized, so dot product = cosine similarity
    self.cosine_similarity = (self.tfidf @ self.tfidf.T).toarray()
    print("Check running")
    return self.cosine_similarity

  def fit(self, col_name: str):
    """Run the full TF-IDF pipeline on the given column."""
    self.buildVocabulary(col_name)
    self.compute_counts(col_name)
    self.compute_tf()
    self.compute_df()
    self.compute_idf()
    self.compute_tfidf()
    return self

  def transform_query(self, query: str):
    """Transform a raw query string into a L2-normalized TF-IDF vector
    using the existing vocabulary and IDF weights."""
    tokens = self._tokenize(query)
    query_counts = np.zeros(len(self.vocab), dtype=np.float32)
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
    """Search the corpus for the top-K most relevant documents."""
    query_vector = self.transform_query(query)

    # sparse @ dense → dense array
    similarities = np.asarray(self.tfidf @ query_vector).ravel()

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
