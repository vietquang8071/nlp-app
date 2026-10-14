# Reflection — Lab 4: Text Classification on IMDB

---

## Tổng quan

Lab 4 thực hiện bài toán **phân loại cảm xúc nhị phân** (positive / negative) trên tập IMDB Movie Reviews (50,000 mẫu) qua 5 thí nghiệm chính, phân tích lỗi và kiểm thử ứng dụng. Toàn bộ quy trình bao gồm: khám phá dữ liệu, xây dựng baseline, so sánh biểu diễn văn bản, phân tích hạn chế của mô hình, và kiểm tra ảnh hưởng của n-gram features.

---

## Những gì đã làm được

### 1. Quy trình EDA bài bản
- Phát hiện tập dữ liệu cân bằng hoàn toàn (50/50), không có missing values.
- Phát hiện **418 bài review trùng lặp** và đã loại bỏ chúng trước khi chia tập train/test (còn 49,582 mẫu), tránh rò rỉ dữ liệu.

### 2. So sánh 3 cấu hình mô hình

| Representation | Classifier | F1 |
| :--- | :--- | :---: |
| TF-IDF | Logistic Regression | 0.8582 |
| Avg Word2Vec | Logistic Regression | 0.8555 |
| **TF-IDF** | **Linear SVM** | **0.8961** |

- TF-IDF + Linear SVM cho kết quả tốt nhất (~90% accuracy).
- Avg Word2Vec + LR xấp xỉ TF-IDF + LR, cho thấy biểu diễn ngữ nghĩa không tự động vượt trội hơn biểu diễn từ vựng trong bài toán sentiment analysis.

### 3. Chứng minh hạn chế của Averaged Embeddings (Experiment 4)
- Cosine similarity giữa `"this movie is good"` và `"this movie is not good"` đạt **0.9633** — gần như trùng nhau.
- Hai câu đảo vị trí `"not bad it is good"` vs `"not good it is bad"` cho cosine similarity = **1.0000** — vector hoàn toàn giống nhau dù nghĩa đối lập.
- Kết luận: Mean pooling **không hiểu thứ tự từ** và **không biểu diễn được phủ định**.

### 4. Đánh giá ảnh hưởng của n-gram (Experiment 5)
- Uni + Bigram (F1 = **0.9069**) vượt Unigram (F1 = **0.8955**) nhờ nắm bắt các cụm từ phủ định/bổ nghĩa.
- Đánh đổi: kích thước từ vựng tăng gấp ~6.7 lần (33,549 → 224,227), thời gian huấn luyện tăng gấp ~2.4 lần.

### 5. Phân tích trọng số mô hình (Inspect Weights)
- Top positive features (`excellent`, `great`, `perfect`) và top negative features (`worst`, `bad`, `awful`) khớp trực giác con người.
- Phát hiện một số features trung tính nhưng mang trọng số cao do tương quan thống kê trong tập huấn luyện (`today`, `minutes`).

### 6. Xây dựng `Word2VecVectorizer` tuân chuẩn Scikit-Learn API
- Kế thừa `BaseEstimator` và `TransformerMixin`, tích hợp `check_is_fitted`.
- Có tiền xử lý loại bỏ thẻ HTML, tận dụng đa nhân CPU.

---

## Bài học rút ra

1. **Representation phụ thuộc vào bài toán**: TF-IDF giữ lại tín hiệu từ vựng mạnh cho sentiment analysis, trong khi Word2Vec average làm mờ các tín hiệu đó.
2. **Phủ định là điểm yếu cốt lõi của Bag-of-Words**: Cả TF-IDF unigram lẫn averaged embeddings đều không mô hình hóa được mối quan hệ `not + adjective`. Bigram khắc phục một phần, nhưng không triệt để.
3. **Classifier cũng quan trọng không kém representation**: Cùng dùng TF-IDF, Linear SVM vượt trội Logistic Regression (~3.8% F1), cho thấy lựa chọn bộ phân loại ảnh hưởng đáng kể.
4. **Làm sạch dữ liệu trước khi chia tập**: Nếu không loại bỏ trùng lặp, cùng một bài review có thể xuất hiện ở cả train và test, gây rò rỉ dữ liệu và đánh giá lạc quan ảo.

---

## Hạn chế còn tồn tại

- **Chưa làm sạch thẻ HTML trong pipeline TF-IDF**: Từ `"br"` (từ thẻ `<br />`) vẫn có thể lọt vào từ vựng. Chỉ có `Word2VecVectorizer` mới có bước loại bỏ HTML.
- **Chưa thử pre-trained embeddings**: Word2Vec được huấn luyện từ đầu trên tập IMDB nhỏ; nếu dùng GloVe hoặc GoogleNews pre-trained, chất lượng biểu diễn có thể tốt hơn đáng kể.
- **Chưa thử mô hình có khả năng nắm bắt ngữ cảnh**: LSTM, BiLSTM, hoặc Transformer (BERT) có thể giải quyết triệt để vấn đề thứ tự từ và phủ định.
- **Số lượng mẫu kiểm thử ứng dụng (df_app) còn ít**: Chỉ 10 câu, chưa đủ đại diện để kết luận mạnh về khả năng tổng quát hóa của mô hình.

---

## Kết luận

Lab 4 cung cấp cái nhìn toàn diện về pipeline phân loại văn bản truyền thống: từ EDA, làm sạch dữ liệu, so sánh representation (sparse vs dense), phân tích hạn chế về thứ tự từ, đến đánh giá ảnh hưởng của n-gram features. Kết quả tốt nhất đạt được là **TF-IDF + Linear SVM** với F1 macro = **0.8961**. Các thí nghiệm về word order và n-gram cho thấy rõ giới hạn của các phương pháp Bag-of-Words, mở ra hướng phát triển tiếp theo với các mô hình có khả năng biểu diễn ngữ cảnh và thứ tự từ.

