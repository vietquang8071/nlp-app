# Prediction trước Experiment — Transformer

## Prediction 1
**Một Transformer có thể xử lý các token trong sequence song song hơn RNN không?**

- **Prediction:** Có.
- **Reason:** RNN phải phụ thuộc vào kết quả của bước trước để  có thể tính toán bước sau, trong khi đó Transformers sử dụng cơ chế Attention, các ma trận tham số của Q, K, V có thể tính toán độc lập mà không phụ thuộc vào bước tính toán trước đó.
- **Confidence:** Cao.

## Prediction 2
**Nếu bỏ positional encoding, Transformer có còn biết thứ tự token không?**

- **Prediction:** Không
- **Reason:** Self-Attention không thể nhận biết được thứ tự các token trong 1 câu do các token được xử lý song song. Positional Encoding giúp cho Transformer biết được token nào ở vị trí nào.
- **Confidence:** Cao

## Prediction 3
**Nếu hai câu có cùng tập token nhưng khác thứ tự, Transformer không có positional information có thể phân biệt chúng không?**

- **Prediction:** Không
- **Reason:** Như prediction 2
- **Confidence:** Cao

## Prediction 4
**Hai attention heads có nhất thiết học cùng một attention pattern không?**

- **Prediction:** Không.
- **Reason:** Mỗi attention head có các ma trận trọng số  của Q, K, V khác nhau.
- **Confidence:** Cao

## Prediction 5
**Tăng số attention heads có chắc chắn làm accuracy tăng không?**

- **Prediction:** Không.
- **Reason:** Accuracy còn phụ thuộc vào nhiều yếu tố khác, bên cạnh đó, tăng attention heads đồng nghĩa với việc mô hình trở nên phức tạp hơn, dẫn đến overfit. 
- **Confidence:** Cao.

## Prediction 6
**Transformer có luôn nhanh hơn RNN trên mọi sequence length không?**

- **Prediction:** Không.
- **Reason:** Nhược điểm của Transformers chính là thời gian tính toán tăng theo bình phương của sequence length. 
- **Confidence:** Cao.