# Reflection — N-gram Language Model

> Các câu trả lời dưới đây dựa trên thực nghiệm với corpus C4 (30K documents, ~12.5M tokens, vocab ~260K) sử dụng Bigram và Trigram với MLE và Laplace Smoothing.

---

## Câu 1: Nếu tăng n, mô hình nhận thêm thông tin gì?

Khi tăng n, mô hình nhận thêm **context dài hơn** — tức là nhiều từ phía trước hơn để dự đoán từ tiếp theo.

- **Bigram (n=2):** chỉ nhìn 1 từ trước đó → P(w | w₋₁)
- **Trigram (n=3):** nhìn 2 từ trước đó → P(w | w₋₂, w₋₁)

Context dài hơn giúp model nắm bắt được **các phụ thuộc xa hơn giữa các từ**, từ đó dự đoán chính xác hơn. Ví dụ trong thí nghiệm, trigram dự đoán đúng `"natural language" → "processing"` vì nhìn được cả 2 từ context, trong khi bigram chỉ nhìn `"language"` → có thể cho kết quả kém hơn.

---

## Câu 2: Tại sao tăng n lại làm sparsity tăng?

Khi tăng n, **số lượng tổ hợp n-gram có thể có tăng theo cấp số nhân** (lên đến V^n), nhưng corpus thì hữu hạn.

Từ kết quả thống kê thực tế:

| N-gram | Số lượng unique | Xuất hiện 1 lần |
|--------|----------------|-----------------|
| Unigram | 259,813 | 146,246 (56%) |
| Bigram | 2,875,278 | 2,012,659 (70%) |
| Trigram | 7,679,362 | 6,521,490 (85%) |

Trigram có đến **85% chỉ xuất hiện 1 lần** (hapax legomena). Càng tăng n, càng nhiều n-gram chưa từng xuất hiện trong corpus → **dữ liệu thưa thớt** (sparse), khiến việc ước lượng xác suất không đáng tin cậy. Đây chính là lý do Trigram MLE cho PPL = ∞ trên valid/test — chỉ cần 1 trigram chưa thấy là toàn bộ câu có P = 0.

---

## Câu 3: Tại sao smoothing cần thiết?

Smoothing cần thiết để **xử lý vấn đề zero probability** — khi model gặp n-gram chưa từng xuất hiện trong training data.

Với MLE (không smoothing):
- Nếu gặp n-gram mới → P = 0 → log(0) = -∞ → perplexity = ∞
- Kết quả thực tế: Trigram MLE cho PPL = ∞ trên cả valid và test set

Với Laplace smoothing:
- Mọi n-gram đều có P > 0 (cộng thêm 1 vào count)
- Trigram Laplace: Valid PPL = 110,091 — rất cao nhưng ít nhất vẫn là số hữu hạn, có thể dùng để so sánh

Nói cách khác, **không có smoothing thì model hoàn toàn thất bại** trên dữ liệu mới vì chắc chắn sẽ gặp n-gram chưa thấy.

---

## Câu 4: Perplexity đo điều gì?

Perplexity đo **mức độ "bất ngờ" trung bình** của model khi gặp từ tiếp theo trong câu. Công thức:

$$PPL = \exp\left(-\frac{1}{N}\sum_{i=1}^{N}\log P(w_i \mid \text{context})\right)$$

- **PPL thấp** → model ít bất ngờ → dự đoán tốt, xác suất cao cho từ đúng
- **PPL cao** → model rất bất ngờ → dự đoán kém

Có thể hiểu trực quan: perplexity ≈ số lượng từ mà model "do dự" khi chọn. PPL = 10 nghĩa là model như đang chọn ngẫu nhiên giữa 10 từ, PPL = 100 là giữa 100 từ.

Kết quả thực tế: Trigram MLE có Train PPL = 11.41 (rất tốt vì đã "nhớ" hết training data), nhưng Bigram MLE Train PPL = 153.98 (kém hơn vì context ngắn).

---

## Câu 5: Một model có perplexity thấp hơn có luôn tạo ra văn bản tốt hơn đối với con người không?

**Không, không luôn luôn.** Có nhiều lý do:

1. **Overfitting:** Trigram MLE có Train PPL = 11.41 (cực thấp) nhưng Valid/Test PPL = ∞. Model "nhớ" training data nhưng không tổng quát hóa được → văn bản sinh ra có thể lặp lại training data thay vì sáng tạo.

2. **Perplexity không đo chất lượng ngữ nghĩa:** Một câu có thể đúng ngữ pháp, xác suất cao, nhưng vô nghĩa hoặc nhàm chán. Perplexity chỉ đo mức phù hợp thống kê, không đo sự mạch lạc, sáng tạo, hay thú vị.

3. **Domain-specific:** Model train trên web text (C4) sẽ có PPL thấp trên web text nhưng có thể sinh ra văn bản không phù hợp cho domain khác (y tế, pháp luật...).

4. **Đánh giá con người là chủ quan:** Con người đánh giá văn bản dựa trên nhiều tiêu chí (logic, sáng tạo, phong cách, cảm xúc) mà perplexity không capture được.

---

## Câu 6: N-gram language model thất bại ở đâu khi so với cách con người hiểu ngôn ngữ?

N-gram thất bại ở nhiều khía cạnh:

1. **Không hiểu ngữ nghĩa:** N-gram chỉ đếm tần suất chuỗi từ, không hiểu **ý nghĩa**. Ví dụ, model không biết "bank" trong "river bank" khác "bank account".

2. **Context cố định và quá ngắn:** Trigram chỉ nhìn 2 từ trước. Con người có thể nhớ và liên kết thông tin từ nhiều câu, nhiều đoạn, thậm chí nhiều trang trước đó.

3. **Không có khả năng suy luận:** Con người có thể suy ra ý nghĩa từ ngữ cảnh, kiến thức nền, logic. N-gram chỉ dựa vào thống kê đơn thuần.

4. **Không xử lý được long-range dependencies:** Ví dụ: "The cat, which was sitting on the mat and purring softly, **was**..." — con người biết "was" liên quan đến "cat" ở đầu câu, nhưng trigram chỉ nhìn "softly ," → không liên kết được.

5. **Không hiểu cấu trúc ngữ pháp:** N-gram xử lý ngôn ngữ như chuỗi phẳng, không hiểu cây cú pháp, quan hệ chủ-vị, bổ ngữ...

6. **Không có world knowledge:** Con người hiểu "mặt trời mọc ở phía đông" nhờ kiến thức thế giới, N-gram chỉ biết nếu cụm từ đó xuất hiện trong corpus.

---

## Câu 7: Nếu context dài 100 từ, trigram có sử dụng được thông tin của 97 từ đầu không?

**Không.** Trigram chỉ sử dụng **2 từ cuối cùng** (n-1 = 2) làm context để dự đoán từ tiếp theo. 97 từ đầu tiên bị **bỏ qua hoàn toàn**.

Điều này thể hiện rõ trong code [`NGramLanguageModel.py`](file:///home/vitquay1708/Study_Space/NLP/lab2/NGramLanguageModel.py#L100-L101):

```python
context = context[-(self.n - 1):]  # Chỉ lấy n-1 từ cuối
```

Đây chính là **hạn chế cốt lõi** của N-gram model: giả định Markov bậc n-1 — xác suất từ tiếp theo chỉ phụ thuộc vào n-1 từ ngay trước đó. Mọi thông tin xa hơn đều bị mất.

Để giải quyết vấn đề này, các kiến trúc hiện đại như **RNN, LSTM, Transformer** được sử dụng — chúng có khả năng nhớ và xử lý context dài hơn rất nhiều.
