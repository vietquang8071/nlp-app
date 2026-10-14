# Prediction 1: TF-IDF + Logistic Regression có khả năng hoạt động tốt không?
Answer: Không tốt.
Reason: Việc sử dụng TF-IDF để vector hóa văn bản sẽ không có yếu tố ngữ nghĩa, dẫn đến khả năng hiểu ngữ cảnh yếu.
Confidence: Cao.
# Prediction 2: Average Word2Vec có chắc chắn tốt hơn TF-IDF không?
Answer: Không chắc chắn.
Reason: Bởi sử dụng Vectorizer nào còn phụ thuộc vào dữ liệu, bài toán. Ví dụ, các dữ liệu mà có từ khóa xuất hiện trực tiếp là tín hiệu quan trọng để phân loại, thì TF-IDF sẽ tốt hơn bới Word2Vec (average) sẽ làm bão hòa tín hiệu các từ đó khi lấy trung bình.
Confidence: Cao.
# Prediction 3: Nếu tăng vocabulary size thì accuracy chắc chắn tăng không?
Answer: Chưa chắc.
Reason: Vocab tăng dẫn đến vector size tăng. Tuy nhiên còn phải xét đến liệu rằng phương pháp vectorize đó có phù hợp với bài toán không. Nếu không phù hợp thì khi tăng vocab lên chỉ làm mất thêm thời gian tính toán.
Confidence: Cao.
# Prediction 4: Nếu bỏ stopwords thì performance chắc chắn tăng không?
Answer: Chưa chắc, còn phụ thuộc vào các stop word đó là gì.
Reason: Nếu các stopword đó là các từ/tokens như the, a,... tức là các từ không có vai trò lớn trong ý nghĩa của câu thì có thể performance sẽ tăng. Nhưng nếu là các tử có tính khẳng định/phủ định như not, yes, no,... thì sẽ làm giảm performance do những từ này ảnh hưởng lớn tới kết quả phân loại của mô hình.
Confidence: Cao.
# Prediction 5: Accuracy và F1 có thể cho kết luận khác nhau không?
Answer: Có.
Reason: Ví dụ rõ ràng nhất là một bộ dữ liệu mất cân bằng, 95% mẫu có label là 1, 5% có label là 0. Khi đó, mô hình có thể dự đoán 100% mẫu có label là 1, accuracy của mô hình lúc đó sẽ là 95%, nhưng precision và recall thấp dẫn đến F1-score thấp.
Confidence: Cao.