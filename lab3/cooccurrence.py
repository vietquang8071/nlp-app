import numpy as np
from collections import Counter
from scipy.sparse import dok_matrix, csr_matrix
from typing import List, Tuple, Dict

class MyCooccurrence:
  def __init__(self):
    self.word2id = {}
    self.id2word = {}
    self.matrix = None
    self.vocab_size = 0

  def build_vocabulary(self, corpus, min_count=1):
    word_count = Counter()

    for sen in corpus:
      word_count.update(sen)

    valid_words = sorted([word for word, count in word_count.items() if count >= min_count], key=lambda x: (-word_count[x], x))
    
    for idx, word in enumerate(valid_words):
      self.word2id[word] = idx
      self.id2word[idx] = word
    self.vocab_size = len(self.word2id)


  def build_cooccurrence_matrix(self, corpus: List[List[str]], window_size: int) -> None:
    if self.vocab_size == 0:
      raise ValueError("Vocabulary is empty. Run build_vocabulary() first.")
    from collections import defaultdict
    from scipy.sparse import coo_matrix
    cooc_dict = defaultdict(float)
    for sentence in corpus:
      sentence_ids = [self.word2id[w] for w in sentence if w in self.word2id]
      length = len(sentence_ids)
      
      for i in range(length):
        target_id = sentence_ids[i]
        window_start = max(0, i - window_size)
        window_end = min(length, i + window_size + 1)
        for j in range(window_start, window_end):
          if i == j:
            continue
          context_id = sentence_ids[j]
          cooc_dict[(target_id, context_id)] += 1.0
    rows = []
    cols = []
    data = []
    for (r, c), value in cooc_dict.items():
      rows.append(r)
      cols.append(c)
      data.append(value)
    self.matrix = coo_matrix(
      (data, (rows, cols)), 
      shape=(self.vocab_size, self.vocab_size)
    ).tocsr()

  @staticmethod
  def cosine_similarity(vec_a, vec_b):
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if (norm_a == 0 or norm_b == 0):
      return 0.0
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))

  def most_similar(self, word, top_k=5):
    if word not in self.word2id:
      raise KeyError(f"Word '{word}' not in vocabulary")
    target_id = self.word2id[word]
    target_vec = self.matrix[target_id].toarray().flatten()
    target_norm = np.linalg.norm(target_vec)
    if target_norm == 0:
      return []

    dot_products = self.matrix.dot(target_vec)
    row_norms = np.sqrt(np.array(self.matrix.power(2).sum(axis=1)).flatten())
    similarities = dot_products / (target_norm * row_norms + 1e-9)
    best_indices = np.argsort(similarities)[::-1]

    results = []
    for idx in best_indices:
      if idx == target_id:
        continue
      results.append((self.id2word[idx], float(similarities[idx])))
      if len(results) == top_k:
        break
    return results
