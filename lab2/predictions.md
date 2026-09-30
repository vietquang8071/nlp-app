# Prediction trước Experiment

> **Lưu ý:** Các prediction dưới đây được đưa ra **trước khi chạy code/experiment**. Sau experiment sẽ đối chiếu kết quả thực tế và cập nhật prediction nếu cần.

---

## Prediction 1 — Vocabulary

**Question:** Khi chuyển từ Unigram → Bigram → Trigram, vocabulary có tăng không?

**Prediction:** Không, vocabulary **không tăng đáng kể / không thay đổi** nếu sử dụng cùng một corpus và cùng cách preprocessing.

**Reason:** Vocabulary được tạo từ tập các **từ (unique tokens)** xuất hiện trong corpus. Việc chuyển từ Unigram sang Bigram hoặc Trigram chỉ thay đổi cách kết hợp các từ thành n-gram, không tạo ra từ mới.

**Confidence:** High

---

## Prediction 2 — Số lượng n-gram

**Question:** Số lượng n-gram sẽ thay đổi như thế nào khi tăng n từ Unigram → Bigram → Trigram?

**Prediction:** Số lượng **distinct n-gram** sẽ tăng từ Unigram → Bigram → Trigram.

**Reason:** Khi tăng kích thước context, số tổ hợp có thể xuất hiện tăng lên. Bigram xét từng cặp từ liên tiếp, trong khi Trigram xét từng bộ ba từ liên tiếp. Do đó, trong cùng một corpus, số lượng các n-gram khác nhau có xu hướng tăng theo n.

**Confidence:** High

---

## Prediction 3 — Zero Probability

**Question:** Mô hình nào có khả năng gặp zero probability nhiều hơn?

**Prediction:** **Trigram** có khả năng gặp zero probability nhiều hơn Bigram, và Bigram nhiều hơn Unigram.

**Reason:** Khi n tăng, n-gram trở nên cụ thể hơn và ít có khả năng xuất hiện trong corpus. Vì vậy, với corpus hữu hạn, nhiều Bigram/Trigram có thể không được quan sát. Với MLE, một n-gram chưa xuất hiện sẽ có xác suất bằng 0.

\[
P(w_i|w_{i-n+1}^{i-1}) = 0
\]

nếu n-gram tương ứng chưa xuất hiện trong training corpus.

**Confidence:** High

---

## Prediction 4 — Perplexity trên Training Set

**Question:** Mô hình nào dự kiến có perplexity thấp hơn trên training set?

**Prediction:** **Trigram** dự kiến có perplexity thấp hơn Bigram và Unigram trên training set, nếu xử lý zero probability phù hợp (ví dụ sử dụng smoothing).

**Reason:** Trigram sử dụng context dài hơn nên có thể mô hình hóa các phụ thuộc giữa các từ cụ thể hơn. Ngoài ra, mô hình có nhiều tham số hơn và có khả năng fit training data tốt hơn.

Do đó, dự kiến:

\[
PPL_{\text{trigram}}
<
PPL_{\text{bigram}}
<
PPL_{\text{unigram}}
\]

trên training set.

**Confidence:** Medium

---

## Prediction 5 — Corpus nhỏ

**Question:** Nếu corpus rất nhỏ, Trigram có chắc chắn tốt hơn Bigram không?

**Prediction:** **Không. Trigram không chắc chắn tốt hơn Bigram**, đặc biệt khi corpus rất nhỏ.

**Reason:** Trigram sử dụng context dài hơn nên cần nhiều dữ liệu hơn để quan sát đầy đủ các tổ hợp từ. Với corpus nhỏ, rất nhiều trigram có thể chưa từng xuất hiện, dẫn đến:

- nhiều zero probability;
- dữ liệu thưa (sparsity);
- khó ước lượng xác suất đáng tin cậy;
- có nguy cơ overfitting.

Bigram sử dụng context ngắn hơn nên thường có nhiều dữ liệu hơn cho mỗi context.

Vì vậy, dù Trigram có thể fit training data tốt hơn, điều đó **không đảm bảo** nó hoạt động tốt hơn trên dữ liệu chưa thấy.

**Confidence:** High

---

# Summary of Predictions

| Prediction | Dự đoán | Confidence |
|---|---|---|
| Vocabulary | Không tăng khi tăng n | High |
| Số lượng n-gram | Tăng khi n tăng | High |
| Zero probability | Trigram > Bigram > Unigram | High |
| Training perplexity | Trigram dự kiến thấp hơn | Medium |
| Corpus nhỏ | Trigram không chắc chắn tốt hơn Bigram | High |

> **Sau experiment:** Đối chiếu kết quả thực tế với các prediction trên và ghi rõ prediction nào được xác nhận, prediction nào không được xác nhận, cùng với nguyên nhân.