# Reflection — Từ TF-IDF đến Transformer

## 1. TF-IDF

**Limitation:** TF-IDF biểu diễn văn bản dựa trên tần suất xuất hiện của từ, nên không nắm bắt được ngữ nghĩa, ngữ cảnh hay thứ tự từ. Các từ đồng nghĩa thường được coi là những đặc trưng độc lập, còn hai câu có cùng từ nhưng khác thứ tự có thể có biểu diễn giống nhau.

**Hướng cải thiện:** Word2Vec học biểu diễn vector liên tục để thể hiện mức độ tương đồng ngữ nghĩa giữa các từ.

## 2. Word2Vec

**Limitation:** Word2Vec tạo một vector cố định cho mỗi từ, bất kể từ đó xuất hiện trong ngữ cảnh nào. Vì vậy, nó khó biểu diễn hiện tượng đa nghĩa và chưa tự mô hình hóa thứ tự hay quan hệ giữa các từ trong toàn bộ câu.

**Hướng cải thiện:** LSTM xử lý chuỗi token theo thứ tự và xây dựng biểu diễn phụ thuộc ngữ cảnh thông qua trạng thái ẩn.

## 3. LSTM

**Limitation:** LSTM xử lý chuỗi tuần tự nên khó song song hóa theo chiều thời gian, dẫn đến thời gian huấn luyện có thể lớn. Dù cơ chế cổng giúp giảm vấn đề mất thông tin, LSTM vẫn có thể gặp khó khăn khi học các quan hệ phụ thuộc rất xa trong chuỗi dài.

**Hướng cải thiện:** Cơ chế Attention cho phép mô hình tập trung trực tiếp vào những vị trí liên quan thay vì chỉ phụ thuộc vào một biểu diễn trạng thái ẩn tổng hợp.

## 4. Attention

**Limitation:** Attention là một cơ chế tổng hợp thông tin, chưa phải một kiến trúc hoàn chỉnh. Đặc biệt, self-attention hai chiều thuần túy không có thông tin vị trí mang tính *permutation-equivariant*: hoán đổi thứ tự token chỉ làm hoán đổi tương ứng các đầu ra. Vì vậy, nếu không có positional information, nó không tự nhận biết được thứ tự từ.

**Hướng cải thiện:** Transformer kết hợp Multi-Head Self-Attention, Positional Encoding, Feed-Forward Network, Residual Connections và Layer Normalization để học biểu diễn ngữ cảnh của toàn bộ chuỗi.

## 5. Transformer

**Remaining limitation:** Self-attention tiêu chuẩn tạo attention scores với kích thước \(T \times T\), khiến chi phí tính toán của attention tăng theo \(O(T^2)\) khi độ dài chuỗi \(T\) tăng (với kích thước biểu diễn cố định). Nếu lưu ma trận attention đầy đủ, bộ nhớ cho ma trận này cũng tăng theo \(O(T^2)\). Transformer còn có thể đòi hỏi nhiều dữ liệu và tài nguyên huấn luyện; tăng độ dài chuỗi, số heads hay số tham số không đảm bảo cải thiện hiệu suất.

## 6. Tổng kết

```text
TF-IDF
  ↓ Limitation: Không biểu diễn ngữ nghĩa, ngữ cảnh và thứ tự từ
Word2Vec
  ↓ Limitation: Embedding tĩnh, không phụ thuộc ngữ cảnh
LSTM
  ↓ Limitation: Xử lý tuần tự, khó song song hóa và học phụ thuộc rất xa
Attention
  ↓ Limitation: Self-attention thuần túy không tự mã hóa thứ tự token
Transformer
  ↓ Remaining limitation: Chi phí attention tăng theo T²; tốn tài nguyên,
    ngữ cảnh dài hơn không đồng nghĩa với dự đoán tốt hơn
```

**Reflection:** Mỗi phương pháp ra đời nhằm khắc phục một số giới hạn của phương pháp trước đó, nhưng không loại bỏ mọi hạn chế. Trong các thí nghiệm phân loại cảm xúc, sự khác biệt về accuracy, F1 và thời gian huấn luyện cho thấy lựa chọn kiến trúc phải dựa trên dữ liệu, mục tiêu và ngân sách tính toán, thay vì mặc định mô hình mới hơn luôn tốt hơn.
