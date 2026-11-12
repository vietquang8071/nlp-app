# Prediction 1: Nếu sử dụng pretrained Transformer thay vì một classifier đơn giản dựa trên word features, NER sẽ thay đổi như thế nào?
## Dự đoán: Pretrained Transformer sẽ đạt Precision, Recall và F1-score cao hơn so với classifier đơn giản dựa trên word features.

## Giải thích:

Một classifier truyền thống thường sử dụng các đặc trưng như chữ viết hoa, tiền tố, hậu tố, từ hiện tại và các từ lân cận. Các đặc trưng này có thể không biểu diễn đầy đủ ngữ nghĩa và sự phụ thuộc vào ngữ cảnh.

Ngược lại, pretrained Transformer sử dụng cơ chế Self-Attention để xây dựng contextual embeddings, giúp một từ có biểu diễn khác nhau tùy theo ngữ cảnh.
# Prediction 2: Các entity dài nhiều token sẽ dễ hay khó hơn entity chỉ có một token?
## Dự đoán: Entity dài nhiều token thường khó nhận dạng chính xác hơn entity chỉ có một token.

## Giải thích:

Với entity một token như Microsoft, mô hình chỉ cần xác định vị trí và phân loại một thực thể tương đối đơn giản.

Tuy nhiên, với United Nations Security Council, mô hình phải xác định chính xác cả điểm bắt đầu, điểm kết thúc và loại thực thể. Tuy nhiên, một số tên dài phổ biến vẫn có thể dễ nhận dạng nhờ ngữ cảnh rõ ràng.

# Prediction 3: Entity hiếm xuất hiện trong training data có khả năng gây lỗi nhiều hơn không?
## Dự đoán: Các entity hiếm xuất hiện trong training data có khả năng bị nhận dạng sai nhiều hơn các entity xuất hiện thường xuyên.

## Giải thích:

Khi một entity xuất hiện nhiều lần trong training data, mô hình có nhiều cơ hội học được các đặc trưng liên quan đến tên, loại thực thể và ngữ cảnh xuất hiện.

Ngược lại, các entity hiếm có ít ví dụ gán nhãn hơn, khiến mô hình khó học được cách nhận dạng và phân loại chính xác.

Ví dụ:
- Microsoft: Xuất hiện nhiều lần trong training data.
- Xylora Technologies: Chỉ xuất hiện một lần hoặc chưa từng xuất hiện.
Mô hình có thể nhận dạng Microsoft chính xác hơn do đã quan sát nhiều ví dụ trong quá trình huấn luyện.

Tuy nhiên, pretrained Transformer có thể giảm vấn đề này nhờ subword tokenization và kiến thức học được trong pretraining. Chẳng hạn, ngay cả khi chưa gặp Xylora Technologies, mô hình vẫn có thể suy luận đây là tổ chức dựa trên hậu tố Technologies và ngữ cảnh xung quanh.