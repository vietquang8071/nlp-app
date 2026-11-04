# Experiment 1:
Câu hỏi: Nếu chỉ dùng self-attention và không có positional information, tại sao thứ tự trở thành vấn đề?
Trả lời: Nếu chỉ sử dụng Self-Attention mà không có Positional Information, mô hình sẽ không thể nhận biết thứ tự xuất hiện của các token trong chuỗi. Nguyên nhân là Self-Attention có tính chất: Khi thay đổi thứ tự các token đầu vào, các representation đầu ra cũng chỉ bị hoán đổi tương ứng, thay vì thay đổi theo vị trí mới. Điều này được chứng minh ở Experiment 1 và thí nghiệm hoán đổi từ 
# Experiment 2 — Number of attention heads

## Câu 1: Tăng số attention heads có đồng nghĩa với tăng representation dimension không?

Không. Khi giữ nguyên d_model, việc tăng số lượng attention heads không làm tăng tổng số chiều biểu diễn (representation dimension). Thay vào đó, không gian biểu diễn được chia thành nhiều heads, mỗi head có số chiều nhỏ hơn. Sau khi concatenate các attention heads, tổng representation dimension vẫn bằng d_model.

## Câu 2: Khi d_model cố định, tăng số heads làm d_k thay đổi như thế nào?

Khi d_model cố định, số chiều của mỗi attention head d_k giảm tỷ lệ nghịch với số lượng heads:
\[ d_k=\frac{d\_{model}}{n\_{heads}} \]
Như vậy, khi số heads tăng gấp đôi, d_k giảm một nửa.

# Experiment 3 — Attention Head Diversity

## 1. Phân tích từng Attention Head

| Head | Mức độ tập trung | Đặc điểm quan sát |
|---|---|---|
| Head 1 | Phân tán tương đối | Attention phân bổ trên nhiều token, xuất hiện một số vùng chú ý nổi bật nhưng không tập trung vào một cột duy nhất. |
| Head 2 | Rất tập trung tại một số vị trí | Phần lớn attention weights hiển thị rất nhỏ, chỉ có một vài điểm nổi bật tại các token như `angst` và `make`. |
| Head 3 | Tập trung mạnh | Xuất hiện một cột attention nổi bật tại token `sucks`, cho thấy nhiều query tokens chú ý mạnh vào cùng một key token. |
| Head 4 | Tập trung vào một nhóm token | Attention chủ yếu xuất hiện quanh các token `angst`, `comment`, `everything` và một số vị trí lân cận. |

### Head 1 — Attention phân tán

Head 1 có attention weights trải rộng trên nhiều vị trí hơn so với các heads còn lại. Một số query tokens chú ý đến các token như `is`, `really`, `teenage` và `sucks`.

Điều này cho thấy head này có xu hướng phân bổ attention trên nhiều key tokens thay vì tập trung gần như toàn bộ vào một vị trí.

### Head 2 — Attention thưa

Head 2 có phần lớn các ô gần như trắng, chỉ xuất hiện một số attention weights tương đối cao.

Đặc biệt, một số query tokens tập trung vào `angst` hoặc `make`.

Tuy nhiên, không thể kết luận Head 2 không học được thông tin hữu ích chỉ dựa trên heatmap, vì những attention weights nhỏ có thể khó quan sát trên thang màu từ 0 đến 1.

### Head 3 — Attention tập trung mạnh

Head 3 có đặc điểm rõ ràng nhất: nhiều query tokens tập trung attention vào token `sucks`.

Đây là một attention pattern có tính tập trung cao.

Điều này có thể cho thấy Head 3 học được mối liên hệ giữa nhiều token và từ `sucks`, vốn mang sắc thái tiêu cực trong ngữ cảnh này.

Tuy nhiên, chưa thể kết luận head này chuyên xử lý sentiment nếu không có thêm bằng chứng thực nghiệm.

### Head 4 — Attention tập trung vào một nhóm vị trí

Khác với Head 3, Head 4 không tập trung chủ yếu vào một key token duy nhất mà phân bổ các trọng số lớn vào nhiều vị trí khác nhau, đặc biệt quanh `angst`, `comment` và `everything`.

Head này có attention pattern khác biệt tương đối rõ so với Head 1 và Head 3.

## 2. Các Attention Heads có giống nhau không?

**Không hoàn toàn giống nhau.**

Dựa trên các heatmaps:

- **Head 1:** Có attention phân tán hơn so với các heads khác.
- **Head 2:** Attention khá thưa, chỉ một vài vị trí nổi bật.
- **Head 3:** Tập trung rõ rệt vào token `sucks`.
- **Head 4:** Tập trung vào một nhóm key tokens khác nhau.

Những quan sát này cho thấy các attention heads đã học những cách phân bổ attention khác nhau trên cùng một input sequence.

## 3. Có Attention Head nào gần như Redundant không?

Từ các heatmaps hiện tại, chưa có bằng chứng rõ ràng rằng hai heads gần như redundant.

**Question: Multi-Head Attention có thực sự tạo ra các Attention Patterns khác nhau trong experiment của bạn không?**

**Answer:**

Có. Kết quả thực nghiệm cho thấy bốn attention heads đã tạo ra những attention patterns khác nhau trên cùng một input sequence.

Cụ thể:

- Head 1 phân bổ attention tương đối rộng trên nhiều token.
- Head 2 chỉ có một số vị trí attention nổi bật.
- Head 3 tập trung mạnh vào token `sucks`.
- Head 4 tập trung vào một nhóm token như `angst`, `comment` và `everything`.

Sự khác biệt này cho thấy Multi-Head Attention cho phép các heads học những cách phân bổ attention khác nhau để tổng hợp thông tin từ sequence.

Tuy nhiên, chưa thể kết luận mỗi head đảm nhận một chức năng ngữ nghĩa hoặc cú pháp cụ thể, cũng như chưa thể xác định head nào redundant chỉ dựa trên một heatmap.

# Experiment 4: Transformer vs RNN/LSTM
Sự khác biệt về performance giữa LSTM và Transformer có thể xuất phát từ cơ chế xử lý sequence, cách xây dựng sequence representation, cơ chế attention và cấu trúc biến đổi thông tin bên trong mô hình.

LSTM có lợi thế về inductive bias đối với thứ tự token và cơ chế gating để duy trì thông tin theo thời gian. Trong khi đó, Transformer sử dụng Multi-Head Self-Attention để học quan hệ giữa các token một cách song song, kết hợp với Positional Encoding và Feed-Forward Network.

Kết quả thực nghiệm cho thấy LSTM đạt Accuracy (82,94%) và F1-score (82,74%) cao hơn Transformer 4 heads (81,59% và 81,67%), mặc dù Transformer có số tham số lớn hơn. Tuy nhiên, Transformer có thời gian huấn luyện ngắn hơn khoảng 29%.

Như vậy, không có kiến trúc nào luôn vượt trội trên mọi tiêu chí. LSTM cho kết quả phân loại tốt hơn trong lần thực nghiệm này, còn Transformer có lợi thế về thời gian huấn luyện.

# Experiment 5: Sequence length

Transformer không thể giải quyết mọi vấn đề bằng cách tăng sequence length vì chi phí bộ nhớ của attention matrix tăng theo \(O(T^2)\), trong khi hiệu suất mô hình không nhất thiết được cải thiện khi giữ lại nhiều token hơn.

Trong thực nghiệm, khi sequence length tăng từ 32 lên 256, attention memory tăng 64 lần và thời gian huấn luyện tăng khoảng 47.4%. Tuy nhiên, F1-score cao nhất lại đạt được tại max_length = 64, thay vì 256.

Điều này cho thấy việc tăng sequence length có thể bổ sung ngữ cảnh, nhưng cũng làm tăng chi phí tính toán và có thể đưa thêm thông tin không hữu ích vào mô hình.

Vì vậy, cần lựa chọn sequence length phù hợp để cân bằng giữa lượng thông tin được giữ lại, hiệu suất phân loại và chi phí tính toán.

# Experiment 6: Pooling Strategy
Kết quả thực nghiệm cho thấy Pooling Strategy có ảnh hưởng đến hiệu suất Sentiment Classification. Cụ thể, Mean Pooling đạt Accuracy và F1-score là 81,61%, cao hơn CLS-style Pooling với 80,87%, mặc dù cả hai mô hình có cùng số lượng tham số.

Sự khác biệt này có thể xuất phát từ cơ chế tổng hợp thông tin của từng phương pháp. Mean Pooling tổng hợp representations từ tất cả các token hợp lệ, trong khi CLS-style Pooling phụ thuộc vào khả năng học biểu diễn toàn bộ sequence của một token đặc biệt.

Trong thực nghiệm này, Mean Pooling mang lại hiệu suất tốt hơn, cho thấy việc lựa chọn cách xây dựng sequence representation có thể ảnh hưởng đến chất lượng phân loại.