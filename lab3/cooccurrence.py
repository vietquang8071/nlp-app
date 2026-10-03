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
    
    for idx, word in valid_words:
      self.word2id[word] = idx
      self.id2word[idx] = word
    self.vocab_size = len(self.word2id)


  def build_cooccurrence_matrix(self, corpus, window_size):
    if self.vocab_size == 0:
      raise ValueError("Vocabulary is empty")

    sparse_matrix = dok_matrix((self.vocab_size, self.vocab_size), dtype=np.float32)
    for sen in corpus:
      length = len(sen)
      for i in range(length):
        target_word = sen[i]
        if target_word not in self.word2id:
          continue
        target_id = self.word2id[target_word]
        window_start = max(0, i - window_size)
        window_end = min(length, i + window_size + 1)
        for j in range(window_start, window_end):
          if i == j:
            continue
          context_word = sen[j]
          if context_word not in self.word2id:
            continue
          context_id = self.word2id[context_word]
          sparse_matrix[target_id, context_id]+=1.0
          self.matrix = sparse_matrix.tocsr()

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
    similarities = []
    for curr_id in range(self.vocab_size):
      if curr_id == target_id:
        continue
      compare_vec = self.matrix[curr_id].toarray().flatten()
      score = self.cosine_similarity(target_vec, compare_vec)
      curr_word = self.id2word[curr_id]
      similarities.append((curr_word, score))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]
