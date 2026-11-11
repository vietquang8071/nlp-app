# Prediction 1 — Pretrained Transformer vs. Transformer train from scratch

**Câu hỏi:** Một pretrained Transformer được fine-tune trên IMDb có khả năng đạt kết quả tốt hơn Transformer nhỏ được train from scratch trên cùng dữ liệu không?

**Prediction:** **Có.** Pretrained Transformer sau khi fine-tune được kỳ vọng đạt Accuracy và F1-score cao hơn Transformer nhỏ train from scratch.

**Reason:**

- Qua pretraining trên lượng văn bản lớn, mô hình đã học được biểu diễn ngữ nghĩa, quan hệ giữa các từ và nhiều đặc điểm ngữ cảnh. Fine-tuning chỉ cần điều chỉnh những biểu diễn này cho nhiệm vụ phân loại cảm xúc.
- Transformer train from scratch phải học đồng thời đặc trưng ngôn ngữ và ranh giới phân loại từ dữ liệu IMDb. Với lượng dữ liệu huấn luyện và số epoch có hạn, việc này thường khó hơn và dễ bị overfitting.
- Pretraining tạo điểm khởi đầu tốt hơn so với khởi tạo trọng số ngẫu nhiên, giúp mô hình sử dụng dữ liệu có nhãn hiệu quả hơn.

**Expected evidence:**

- Pretrained Transformer có Accuracy và F1-score trên tập test cao hơn mô hình train from scratch.
- Đường validation loss của pretrained model có thể giảm nhanh hơn và ổn định hơn trong các epoch đầu.
- Sự khác biệt được kiểm chứng trên cùng train/validation/test split; nên chạy nhiều random seeds và báo cáo trung bình, độ lệch chuẩn nếu tài nguyên cho phép.

# Prediction 2 — Freeze encoder vs. Full fine-tuning

**Câu hỏi:** Nếu freeze toàn bộ pretrained BERT encoder và chỉ train classification head thì kết quả sẽ như thế nào so với fine-tuning toàn bộ mô hình?

**Prediction:** **C. Kém hơn.** Mô hình chỉ huấn luyện classification head được kỳ vọng có Accuracy và F1-score thấp hơn mô hình fine-tune toàn bộ encoder.

**Reason:**

- Khi freeze encoder, các trọng số BERT không được cập nhật theo nhãn sentiment của IMDb. Classification head chỉ có thể kết hợp những đặc trưng cố định mà encoder đã học trước đó.
- Full fine-tuning cho phép điều chỉnh cả encoder và classification head để nhận biết tốt hơn các tín hiệu cảm xúc đặc thù, như phủ định, mỉa mai hoặc quan hệ giữa các câu trong review.
- Tuy nhiên, frozen encoder thường cần ít bộ nhớ GPU và thời gian huấn luyện hơn vì không phải lưu gradient và cập nhật trọng số encoder. Nếu dữ liệu ít hoặc full fine-tuning chưa được tối ưu, chênh lệch chất lượng có thể nhỏ hoặc đảo chiều.

**Expected evidence:**

- Full fine-tuning có Accuracy và F1-score trên tập test cao hơn phương án frozen encoder.
- Frozen encoder có số tham số *trainable* ít hơn, thời gian mỗi epoch ngắn hơn và mức sử dụng VRAM thấp hơn.
- So sánh trên cùng pretrained checkpoint, tokenizer, data split và quy trình đánh giá; ghi nhận cả chất lượng lẫn chi phí tính toán.

# Prediction 3 — Ảnh hưởng của việc giảm training data

**Câu hỏi:** Khi giảm dữ liệu huấn luyện từ 100% xuống 50%, 25% và 10%, pretrained model hay model train from scratch sẽ giảm performance mạnh hơn?

**Prediction:** **Transformer train from scratch sẽ giảm performance mạnh hơn**, đặc biệt ở mức 25% và 10% dữ liệu. Pretrained model được kỳ vọng giữ Accuracy và F1-score tốt hơn khi số lượng mẫu có nhãn giảm.

**Reason:**

- **Pretraining giúp giảm nhu cầu dữ liệu có nhãn (sample complexity):** pretrained model đã có biểu diễn ngôn ngữ học được từ dữ liệu không gán nhãn, nên chỉ cần một lượng nhỏ ví dụ IMDb để học nhiệm vụ sentiment classification.
- **Train from scratch phụ thuộc nhiều vào dữ liệu có nhãn:** mô hình phải tự học biểu diễn từ vựng, ngữ cảnh và quy tắc phân loại. Khi dữ liệu ít, các biểu diễn dễ thiếu độ bao phủ và mô hình có nguy cơ overfitting.
- **Transfer learning:** kiến thức học từ giai đoạn pretraining có thể được chuyển sang tác vụ IMDb, giúp pretrained model duy trì khả năng tổng quát hóa khi giảm dữ liệu huấn luyện.

**Expected evidence:**

| Tỷ lệ training data | Pretrained Transformer (dự đoán) | Transformer train from scratch (dự đoán) |
|---|---|---|
| 100% | Chất lượng cao; làm mốc so sánh | Thấp hơn pretrained model |
| 50% | Giảm nhẹ hoặc vừa | Giảm rõ hơn |
| 25% | Giảm nhưng vẫn tương đối ổn định | Giảm mạnh |
| 10% | Giảm đáng kể so với 100%, nhưng có lợi thế từ pretraining | Giảm mạnh nhất; có nguy cơ overfitting cao |

Đo **Accuracy** và **F1-score** của từng mô hình tại cả bốn tỷ lệ, rồi tính mức giảm so với 100%:

\[
\Delta F1(p) = F1(100\%) - F1(p), \quad p \in \{50\%,25\%,10\%\}.
\]

Giả thuyết được ủng hộ nếu ở cùng tỷ lệ dữ liệu, mức giảm F1 của mô hình train from scratch **lớn hơn** pretrained model. Nên biểu diễn cả hai đường F1 theo tỷ lệ training data để quan sát xu hướng.

# Nguyên tắc kiểm chứng

- Giữ nguyên **tập validation và test** giữa các thí nghiệm; chỉ thay đổi tỷ lệ tập train ở Prediction 3.
- Lấy các tập 10%, 25%, 50% bằng **stratified sampling** để giữ tỷ lệ nhãn tích cực/tiêu cực; nếu có thể, sử dụng các tập con lồng nhau để so sánh nhất quán.
- Giữ các yếu tố so sánh hợp lý và công bố khác biệt về kích thước mô hình, tokenizer, số tham số trainable, ngân sách huấn luyện. Chênh lệch giữa pretrained model lớn và scratch model nhỏ **không thể chỉ quy cho pretraining**.
- Ghi nhận **Accuracy, Precision, Recall, F1-score**, thời gian huấn luyện và VRAM; không kết luận chỉ từ Accuracy.
- **Không sửa dự đoán sau khi xem kết quả.** Nếu kết quả khác dự đoán, giải thích bằng các bằng chứng thực nghiệm.
