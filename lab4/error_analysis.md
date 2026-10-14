# Error analysis

## Phạm vi phân tích

Các nhãn `True` và `Predicted` dưới đây được lấy từ các output đã lưu trong
`classification.ipynb`: phần **Application** và thí nghiệm **Word order**.
Do notebook không lưu từng dự đoán của 10,000 mẫu test, ba lỗi bên dưới là ba
**lần dự đoán sai** đã được ghi nhận trực tiếp; trong đó câu `not bad it is good`
sai ở cả hai mô hình khác nhau. Mô hình trong mỗi dòng được nêu rõ để tránh xem
hai kết quả đó là hai văn bản khác nhau.

`confusion_matrix.png` cũng cho thấy lỗi không phải là cá biệt: TF-IDF + LR có
719 lỗi negative -> positive và 656 lỗi positive -> negative; Avg Word2Vec + LR
có lần lượt 748 và 695 lỗi; TF-IDF + Linear SVM tốt nhất nhưng vẫn có 551 và 514
lỗi tương ứng. Vì tập dữ liệu cân bằng (25,000 mẫu mỗi lớp), đây không phải dấu
hiệu của **class imbalance**.

## Correctly classified examples

| # | Text | Model | True | Predicted | Analysis |
| --- | --- | --- | --- | --- | --- |
| 1 | “I loved the story and the brilliant acting.” | Cả 3 mô hình | positive | positive | Các tín hiệu tích cực trực tiếp, `loved` và `brilliant`, nhất quán với nhãn; không có phủ định hay ý nghĩa mỉa mai. |
| 2 | “The movie was boring and terribly disappointing.” | Cả 3 mô hình | negative | negative | `boring`, `terribly`, và `disappointing` là các từ/cụm tiêu cực rõ ràng; bằng chứng từ vựng cùng hướng. |
| 3 | “This is one of the best movies I have ever watched.” | Cả 3 mô hình | positive | positive | Cụm cường độ cao `one of the best` biểu đạt đánh giá tích cực không mơ hồ. |

## Incorrectly classified examples

| # | Text | Model | True | Predicted | Category | Analysis |
| --- | --- | --- | --- | --- | --- |
| 1 | “The characters were dull and the ending was disappointing.” | TF-IDF + Logistic Regression | negative | positive | **short text** | Đây là câu rất ngắn, chỉ có hai tín hiệu âm chính (`dull`, `disappointing`). Với TF-IDF + LR dùng tối đa 1,000 đặc trưng, một hay cả hai từ có thể không được giữ/không đủ trọng số; khi thiếu ngữ cảnh, mô hình nghiêng về lớp positive. Avg Word2Vec + LR và SVM dự đoán đúng cùng câu, nên đây là hạn chế riêng của baseline hơn là lỗi nhãn. |
| 2 | “not bad it is good” | Avg Word2Vec + Logistic Regression | positive | negative | **negation** | Output thí nghiệm Word order cho thấy mô hình dự đoán negative với xác suất 100%. Vector trung bình của Word2Vec không giữ thứ tự từ và không biểu diễn quan hệ giữa `not` và `bad`; vì vậy tín hiệu từ `bad`/`not` lấn át ý nghĩa tích cực của toàn câu. Điều này phù hợp với cosine similarity rất cao giữa “good” và “not good” (0.9636) trong notebook. |
| 3 | “not bad it is good” | TF-IDF + Logistic Regression | positive | negative | **negation** | Cùng văn bản trên cũng bị TF-IDF + LR gán negative (P(positive) = 27.4%). Dù TF-IDF có unigram và bigram, model vẫn không diễn giải được cấu trúc “not bad” trong câu ngắn này; đặc biệt giới hạn 1,000 features có thể khiến bigram hữu ích không được giữ hoặc có trọng số chưa đủ. Đây là lỗi dự đoán độc lập thứ hai trên cùng một input, không phải một ví dụ văn bản mới. |

## Kết luận

Các lỗi quan sát được tập trung vào **phủ định** và **văn bản ngắn**, thay vì
class imbalance. Hướng cải thiện hợp lý là dùng n-gram đầy đủ hơn (không giới
hạn quá thấp số đặc trưng), giữ các cụm phủ định như `not bad`/`not good`, và
dùng mô hình có khả năng biểu diễn thứ tự/ngữ cảnh. Kết quả Experiment 5 hỗ trợ
điều này: unigram + bigram đạt macro F1 0.9124, cao hơn unigram (0.9041).
