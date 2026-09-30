# Results

## 1. So sánh MLE và Smoothing trên 2 mô hình Bigram và Trigram

| Model           | Train PPL | Valid PPL | Test PPL  |
| --------------- | --------- | --------- | --------- |
| Bigram MLE      | 153.98    | 159.60    | 139.69    |
| Bigram Laplace  | 10967.68  | 16327.53  | 16404.43  |
| Trigram MLE     | 11.41     | inf       | inf       |
| Trigram Laplace | 62248.35  | 110091.36 | 109113.05 |

## 2. Perplexity

| Model   | Train Perplexity | Test Perplexity | Validate Perplexity |
| ------- | ---------------- | --------------- | ------------------- |
| unigram | 3274.980196      | 4197.916643     | 4392.250750         |
| bigram  | 10967.679514     | 16404.427026    | 16327.531020        |
| trigram | 62248.353088     | 109113.052655   | 110091.362065       |

## 3. Next Word Prediction

### 3.1. Bigram

**Context: the**

| Rank | Word  | Probability |
| ---- | ----- | ----------- |
| 1    | most  | 0.006181    |
| 2    | same  | 0.006088    |
| 3    | best  | 0.006018    |
| 4    | first | 0.005632    |
| 5    | world | 0.004686    |

**Context: I**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | '    | 0.015468    |
| 2    | have | 0.012908    |
| 3    | am   | 0.010678    |
| 4    | was  | 0.010466    |
| 5    | 'm   | 0.005944    |

**Context: you**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | can  | 0.020339    |
| 2    | are  | 0.015297    |
| 3    | have | 0.012402    |
| 4    | '    | 0.012233    |
| 5    | will | 0.008797    |

**Context: he**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | was  | 0.004577    |
| 2    | is   | 0.002787    |
| 3    | said | 0.002018    |
| 4    | has  | 0.001909    |
| 5    | had  | 0.001713    |

**Context: she**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | was  | 0.002447    |
| 2    | is   | 0.001530    |
| 3    | said | 0.000980    |
| 4    | has  | 0.000951    |
| 5    | had  | 0.000861    |

**Context: we**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | have | 0.007320    |
| 2    | are  | 0.007262    |
| 3    | can  | 0.006016    |
| 4    | '    | 0.005005    |
| 5    | will | 0.004218    |

**Context: they**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | are  | 0.010507    |
| 2    | have | 0.004195    |
| 3    | can  | 0.003920    |
| 4    | were | 0.003489    |
| 5    | '    | 0.003200    |

**Context: this**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | is   | 0.007422    |
| 2    | year | 0.003718    |
| 3    | time | 0.001884    |
| 4    | week | 0.001694    |
| 5    | one  | 0.001510    |

**Context: that**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | the  | 0.017518    |
| 2    | you  | 0.012495    |
| 3    | is   | 0.008848    |
| 4    | I    | 0.007038    |
| 5    | it   | 0.006087    |

**Context: machine**

| Rank | Word     | Probability |
| ---- | -------- | ----------- |
| 1    | learning | 0.000185    |
| 2    | is       | 0.000182    |
| 3    | and      | 0.000170    |
| 4    | that     | 0.000121    |
| 5    | to       | 0.000114    |

### 3.2. Trigram

**Context: the cat**

| Rank | Word  | Probability |
| ---- | ----- | ----------- |
| 1    | box   | 0.000019    |
| 2    | 's    | 0.000015    |
| 3    | can   | 0.000015    |
| 4    | could | 0.000011    |
| 5    | '     | 0.000011    |

**Context: I am**

| Rank | Word  | Probability |
| ---- | ----- | ----------- |
| 1    | not   | 0.000971    |
| 2    | a     | 0.000911    |
| 3    | so    | 0.000525    |
| 4    | going | 0.000397    |
| 5    | sure  | 0.000382    |

**Context: you are**

| Rank | Word    | Probability |
| ---- | ------- | ----------- |
| 1    | looking | 0.001304    |
| 2    | not     | 0.001058    |
| 3    | a       | 0.000968    |
| 4    | in      | 0.000756    |
| 5    | going   | 0.000618    |

**Context: he is**

| Rank | Word  | Probability |
| ---- | ----- | ----------- |
| 1    | a     | 0.000258    |
| 2    | the   | 0.000114    |
| 3    | not   | 0.000110    |
| 4    | still | 0.000064    |
| 5    | in    | 0.000064    |

**Context: she is**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | a    | 0.000140    |
| 2    | the  | 0.000095    |
| 3    | also | 0.000049    |
| 4    | not  | 0.000049    |
| 5    | in   | 0.000034    |

**Context: we are**

| Rank | Word  | Probability |
| ---- | ----- | ----------- |
| 1    | going | 0.000369    |
| 2    | not   | 0.000283    |
| 3    | able  | 0.000279    |
| 4    | in    | 0.000215    |
| 5    | all   | 0.000170    |

**Context: they are**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | not  | 0.000721    |
| 2    | in   | 0.000285    |
| 3    | the  | 0.000255    |
| 4    | a    | 0.000233    |
| 5    | all  | 0.000184    |

**Context: this is**

| Rank | Word | Probability |
| ---- | ---- | ----------- |
| 1    | a    | 0.001386    |
| 2    | the  | 0.001179    |
| 3    | not  | 0.000471    |
| 4    | an   | 0.000324    |
| 5    | one  | 0.000237    |

**Context: machine learning**

| Rank | Word       | Probability |
| ---- | ---------- | ----------- |
| 1    | and        | 0.000027    |
| 2    | models     | 0.000023    |
| 3    | approaches | 0.000019    |
| 4    | algorithm  | 0.000015    |
| 5    | algorithms | 0.000011    |

**Context: natural language**

| Rank | Word             | Probability |
| ---- | ---------------- | ----------- |
| 1    | processing       | 0.000015    |
| 2    | speech           | 0.000008    |
| 3    | analysis         | 0.000008    |
| 4    | -0.31            | 0.000004    |
| 5    | cryptography.ICO | 0.000004    |

### 3.3. Summary

**Bigram Laplace**

| Context | Top-1    | Top-1 Prob | Top-2 | Top-3 |
| ------- | -------- | ---------- | ----- | ----- |
| the     | most     | 0.006181   | same  | best  |
| I       | '        | 0.015468   | have  | am    |
| you     | can      | 0.020339   | are   | have  |
| he      | was      | 0.004577   | is    | said  |
| she     | was      | 0.002447   | is    | said  |
| we      | have     | 0.007320   | are   | can   |
| they    | are      | 0.010507   | have  | can   |
| this    | is       | 0.007422   | year  | time  |
| that    | the      | 0.017518   | you   | is    |
| machine | learning | 0.000185   | is    | and   |

**Trigram Laplace**

| Context          | Top-1      | Top-1 Prob | Top-2  | Top-3      |
| ---------------- | ---------- | ---------- | ------ | ---------- |
| the cat          | box        | 0.000019   | 's     | can        |
| I am             | not        | 0.000971   | a      | so         |
| you are          | looking    | 0.001304   | not    | a          |
| he is            | a          | 0.000258   | the    | not        |
| she is           | a          | 0.000140   | the    | also       |
| we are           | going      | 0.000369   | not    | able       |
| they are         | not        | 0.000721   | in     | the        |
| this is          | a          | 0.001386   | the    | not        |
| machine learning | and        | 0.000027   | models | approaches |
| natural language | processing | 0.000015   | speech | analysis   |

## 4. Sentence Ranking

**Context: "machine learning"**

| Rank | Candidate               | Log Prob |
| ---- | ----------------------- | -------- |
| 1    | banana computer quickly | -49.9239 |
| 2    | studies language models | -49.9239 |
| 3    | is useful for NLP       | -59.5151 |

**Context: "the president"**

| Rank | Candidate            | Log Prob |
| ---- | -------------------- | -------- |
| 1    | of the United States | -43.7787 |
| 2    | said that he will    | -53.3104 |
| 3    | green fly table jump | -62.4050 |

**Context: "natural language"**

| Rank | Candidate                    | Log Prob |
| ---- | ---------------------------- | -------- |
| 1    | processing is a field        | -58.0687 |
| 2    | banana runs quickly computer | -62.4047 |
| 3    | models can understand text   | -62.4049 |

**Context: "deep learning"**

| Rank | Candidate                     | Log Prob |
| ---- | ----------------------------- | -------- |
| 1    | apple table runs quickly      | -62.4047 |
| 2    | models require large datasets | -62.4047 |
| 3    | is a type of machine learning | -75.6897 |

**Context: "the weather"**

| Rank | Candidate                       | Log Prob |
| ---- | ------------------------------- | -------- |
| 1    | is very nice today              | -56.7092 |
| 2    | forecast predicts rain tomorrow | -60.2082 |
| 3    | computer banana studies quickly | -62.4054 |
