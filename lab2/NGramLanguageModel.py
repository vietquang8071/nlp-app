from collections import Counter, defaultdict
from nltk.tokenize import word_tokenize
import string
import numpy as np
import heapq
class NGramLanguageModel:

    def __init__(self, n, smoothing=False):
        self.n = n
        self.vocab = set()
        self.smoothing=smoothing
        self.ngram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)

    def fit(self, corpus):
        """
        corpus: list of str (raw text) hoặc list of list[str] (pre-tokenized)
        """
        if isinstance(corpus, str):
            corpus = [corpus]

        for text in corpus:
            # Nếu text là str → tokenize, nếu là list → đã tokenize sẵn
            tokens = word_tokenize(text) if isinstance(text, str) else list(text)
            tokens = (
                ["BOS"] * (self.n - 1) +
                tokens +
                ["EOS"] 
            )

            self.vocab.update(tokens)
            for i in range(self.n - 1, len(tokens)):
                ngram = tuple(tokens[i -self.n + 1:i+1])
                context = ngram[:-1]
                self.ngram_counts[ngram]+=1
                self.context_counts[context]+=1
        return self
            

    def probability(self, word, context):
        context = tuple(context)
        ngram = context + (word,)
        if not self.smoothing:
            if self.context_counts[context] == 0:
                return 0.0
            return (
                self.ngram_counts[ngram]/
                self.context_counts[context]
            )
        else:
            count_ngram = self.ngram_counts[ngram]
            count_context = self.context_counts[context]
            V = len(self.vocab)
            return (count_ngram + 1) / (count_context + V)


    def _prepare_tokens(self, sentence):
        """Chuẩn bị tokens: nhận str hoặc list, thêm BOS/EOS."""
        tokens = word_tokenize(sentence) if isinstance(sentence, str) else list(sentence)
        return ["BOS"] * (self.n - 1) + tokens + ["EOS"]

    def sentence_probability(self, sentence):
      tokens = self._prepare_tokens(sentence)

      prob = 1.0
      for i in range(self.n - 1, len(tokens)):
          context = tokens[i - self.n + 1:i]
          prob *= self.probability(tokens[i], context)
          if prob == 0:
              return 0.0
      return prob

    def sentence_log_probability(self, sentence):
        tokens = self._prepare_tokens(sentence)

        log_prob = 0.0
        for i in range(self.n - 1, len(tokens)):
            context = tokens[i - self.n + 1:i]
            p = self.probability(tokens[i], context)
            if p == 0:
                return -np.inf
            log_prob += np.log(p)
        return log_prob

    def perplexity(self, sentence):
        tokens = word_tokenize(sentence) if isinstance(sentence, str) else list(sentence)
        N = len(tokens) + 1  # +1 for EOS
        log_prob = self.sentence_log_probability(sentence)
        return np.exp(-log_prob / N)
        

    def predict_next(self, context,):
        context = list(context)

        if len(context) < self.n - 1:
            context = (
                ["BOS"] * (self.n - 1 - len(context)) +
                context
            )
        else:
            context = context[-(self.n - 1):]

        best_word = None
        best_prob = -1.0

        for word in self.vocab:
            if word in ["BOS"]:
                continue

            prob = self.probability(
                word, 
                context,
            )

            if prob > best_prob:
                best_prob = prob
                best_word = word
        return best_word, best_prob

    def predict_top_k(self, context, k=5):
        """
        Dự đoán top-k từ tiếp theo cho context.
        (Bỏ qua các token là dấu câu)
        Args:
            context: list[str] — các từ context (e.g. ["the", "cat"])
            k: int — số lượng từ trả về
            
        Returns:
            list of (word, probability), sắp xếp giảm dần theo probability
        """
        punctuation = set(string.punctuation)
        context = list(context)

        if len(context) < self.n - 1:
            context = (
                ["BOS"] * (self.n - 1 - len(context)) +
                context
            )
        else:
            context = context[-(self.n - 1):]

        word_probs = []
        for word in self.vocab:
            if word == "BOS" or word in punctuation:
                continue
            prob = self.probability(word, context)
            if prob > 0:
                word_probs.append((prob, word))

        top_k = heapq.nlargest(k, word_probs, key=lambda x: x[0])
        return [(word, prob) for prob, word in top_k]