from collections import Counter, defaultdict
from nltk.tokenize import word_tokenize
import numpy as np

class NGramLanguageModel:

    def __init__(self, n, smoothing=False):
        self.n = n
        self.vocab = set()
        self.smoothing=smoothing
        self.ngram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)

    def fit(self, corpus):
        if isinstance(corpus, str):
            corpus = [corpus]

        for text in corpus:
            tokens = word_tokenize(text)
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


    def sentence_probability(self, sentence):
      tokens = word_tokenize(sentence)
      tokens = (
          ["BOS"] * (self.n - 1) +
          tokens +
          ["EOS"]
      )

      prob = 1.0
      for i in range(self.n - 1, len(tokens)):
          ngram = tokens[i - self.n + 1:i + 1]
          context = ngram[:-1]
          prob *= self.probability(tokens[i], context, self.smoothing)
          if prob == 0:
              return 0.0
      return prob

    def sentence_log_probability(self, sentence):
        tokens = word_tokenize(sentence)
        tokens = (
            ["BOS"] * (self.n - 1) +
            tokens +
            ["EOS"]
        )

        log_prob = 0.0
        for i in range(self.n - 1, len(tokens)):
            ngram = tokens[i - self.n + 1:i + 1]
            context = ngram[:-1]
            p = self.probability(tokens[i], context)
            if p == 0:
                return -np.inf
            log_prob += np.log(p)
        return log_prob

    def perplexity(self, sentence):
        tokens = word_tokenize(sentence)
        N = len(tokens) + 1
        log_prob = self.sentence_log_probability(sentence)
        return np.exp(-log_prob/N)
        

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

        