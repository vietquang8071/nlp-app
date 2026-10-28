## Prediction 1 — Dot Product và Attention Weight

Question: Nếu một key có dot product lớn hơn các key khác, attention weight của nó sẽ như thế nào?

Prediction: Key có dot product với Query lớn hơn sẽ nhận attention weight cao hơn các key còn lại.

Reason: Attention sử dụng Softmax để chuyển scores thành xác suất. Softmax là hàm đơn điệu theo từng score khi giữ các score khác cố định, nên score lớn hơn sẽ có attention weight lớn hơn.

Confidence: 99%

## Prediction 2 — Equal Attention Scores

Question: Nếu tất cả scores giống nhau, \\(s=[1,1,1,1]\\), attention weights sẽ như thế nào?

Prediction: Các attention weights sẽ bằng nhau:

\\[ A=[0.25,\ 0.25,\ 0.25,\ 0.25] \\]

Reason: Softmax tính:

\\[ \operatorname{softmax}(s_i)=\frac{e^{s_i}}{\sum_j e^{s_j}} \\]

Vì tất cả scores bằng nhau nên mỗi token nhận \\(1/4=0.25\\) tổng attention weight.

Confidence: 100%

## Prediction 3 — Dominant Attention Score

Question: Nếu một score lớn hơn rất nhiều, \\(s=[1,1,10]\\), attention sẽ tập trung như thế nào?

Prediction: Attention sẽ tập trung gần như hoàn toàn vào token thứ ba.

\\[ A\approx[0.00012,\ 0.00012,\ 0.99975] \\]

Reason: Softmax sử dụng hàm mũ nên score 10 tạo ra giá trị \\(e^{10}\\) lớn hơn rất nhiều so với \\(e^1\\). Vì vậy token thứ ba nhận gần như toàn bộ attention weight.

Confidence: 100%

## Prediction 4 — Sequence Length và Computational Cost

Question: Nếu sequence tăng từ 10 tokens lên 1000 tokens, chi phí tính Attention thay đổi như thế nào?

Prediction: Số phần tử Attention Matrix tăng 10.000 lần.

Reason: Attention Matrix có kích thước \\(T\times T\\), nên số phần tử tăng theo \\(O(T^2)\\).

\\[ T=10 \Rightarrow 10^2=100 \\]

\\[ T=1000 \Rightarrow 1000^2=1{,}000{,}000 \\]

\\[ \frac{1{,}000{,}000}{100}=10{,}000 \\]

Do đó, bộ nhớ lưu Attention Matrix tăng 10.000 lần nếu giữ nguyên dtype, batch size và số attention heads. Chi phí tính toán phần Attention cũng tăng theo bậc hai khi giữ nguyên số chiều đặc trưng, dù thời gian chạy thực tế không nhất thiết tăng đúng 10.000 lần.

Confidence: 100%

## Prediction 5 — Attention và Human Interpretation

Question: Attention có luôn chọn đúng token mà con người cho là quan trọng nhất không?

Prediction: Không. Attention không phải lúc nào cũng tập trung vào token mà con người đánh giá là quan trọng nhất.

Reason: Attention weights được tính từ Query và Key, phụ thuộc vào các biểu diễn vector và tham số đã học của mô hình. Trong khi đó, con người đánh giá mức độ quan trọng của một token dựa trên ngữ nghĩa, ngữ cảnh và mục tiêu của tác vụ. Vì vậy, hai cách đánh giá không nhất thiết trùng nhau. Attention weight cao cũng không tự động chứng minh token có ảnh hưởng nhân quả lớn nhất đến prediction.

Confidence: 99%
