# 27. Error Analysis

## Phạm vi và cách đọc attention

Notebook huấn luyện một `AttentionClassifier` 4 head trên IMDb: 40.000 review train, 5.000 validation, 5.000 test; vocab 20.000 từ và độ dài đầu vào tối đa 100 token. Kết quả test đã lưu là accuracy **0,8362** và F1 **0,8356**. Sáu câu dưới đây là các probe có nhãn kỳ vọng gán thủ công, không phải mẫu ngẫu nhiên lấy từ test split: ba câu trong `test_sentences` của notebook và ba câu chẩn đoán chạy thêm trên cùng model trong kernel đang hoạt động.

`P` dưới đây là xác suất softmax của lớp được nêu; đây không phải xác suất đã hiệu chuẩn. Để tóm tắt attention, lấy trung bình qua các head rồi trung bình attention nhận được ở mỗi key token qua các query. Đây chỉ là thống kê mô tả của attention, không phải phép đo tác động nhân quả lên lớp dự đoán. Token được xem là quan trọng trong phân tích là nhận định ngữ nghĩa của người đánh giá.

Các ảnh BERT trong thư mục thuộc thí nghiệm attention khác, không phải attention của sentiment classifier này. Cell vẽ heatmap sentiment cuối notebook bị `SyntaxError`; các số attention ở đây lấy trực tiếp từ hàm dự đoán và attention của classifier trong kernel, không đọc từ các ảnh BERT.

## 3 dự đoán đúng

| Câu | Nhãn kỳ vọng | Dự đoán | P(lớp dự đoán) | Hiện tượng |
|---|---|---|---:|---|
| “I do not like this movie.” | Negative | Negative | 0,9991 | Phủ định |
| “This film is excellent, entertaining, and deeply moving.” | Positive | Positive | ≈1,0000 | Từ ngữ cảm xúc tường minh |
| “I expected a disaster, but the film was surprisingly brilliant.” | Positive | Positive | 0,9997 | Tương phản cảm xúc / phụ thuộc ngữ cảnh |

### Đối chiếu attention

- **“I do not like this movie.”** Người đọc thường xem `not` và `like` là các token quan trọng. Attention nhận được của `like` là **0,1875**, của `not` là **0,1429**; attention cũng phân tán sang `i` (**0,2112**) và `movie` (**0,1679**). Model dự đoán Negative đúng. Đây là sự phù hợp một phần giữa token phủ định, cụm cảm xúc và output; riêng các trọng số này không chứng minh model đã dùng đúng phạm vi phủ định.
- **“This film is excellent, entertaining, and deeply moving.”** Các cue cảm xúc `excellent` (**0,2566**) và `moving` (**0,1857**) nằm trong hai vị trí nhận attention cao nhất; `entertaining` nhận **0,1007**. Output Positive phù hợp với nhãn và các cue nổi bật. Đây là một trường hợp attention phù hợp với cách đọc của người, nhưng không chứng minh attention tạo ra dự đoán đúng.
- **“I expected a disaster, but the film was surprisingly brilliant.”** Attention nhận được bởi `surprisingly` là **0,1730**, `disaster` **0,1478**, và `brilliant` **0,1445**. Model vẫn dự đoán Positive đúng dù chú ý tới cả cue tiêu cực lẫn tích cực. Điều này phù hợp với output cuối, nhưng các trọng số không cho biết model đã hiểu quan hệ tương phản `but` như thế nào.

## 3 dự đoán sai

| Câu | Nhãn kỳ vọng | Dự đoán | P(Positive) / P(Negative) | Loại lỗi chính |
|---|---|---|---:|---|
| “I like this movie.” | Positive | Negative | 0,0109 / 0,9891 | Domain shift: câu rất ngắn so với review IMDb dài dùng khi huấn luyện |
| “I thought this movie would be bad, but it was actually excellent.” | Positive | Negative | 0,3387 / 0,6613 | Long-range dependency: cần kết hợp hai mệnh đề trái chiều |
| “The movie was not bad; it was actually quite good.” | Positive | Negative | 0,0046 / 0,9954 | Negation: phạm vi `not` và phần đính chính phía sau |

### 1. Câu ngắn lệch khỏi dạng review huấn luyện

Với **“I like this movie.”**, các key nhận attention cao nhất là `like` (**0,2621**) và `movie` (**0,2598**); `i` và `this` lần lượt nhận **0,2489** và **0,2293**. `like` là cue tích cực mà người đọc thường ưu tiên, nên attention có vẻ phù hợp một phần, nhưng model vẫn dự đoán Negative với P=**0,9891**.

**Giả thuyết:** đầu vào bốn token khác phân phối với các review IMDb dài mà model được huấn luyện trên đó, nên biểu diễn hoặc quyết định cuối có thể không tổng quát tốt cho câu ngắn. **Đối chiếu:** model không bỏ qua hẳn `like` theo thống kê attention, nhưng output vẫn sai và rất chắc theo softmax. Vì vậy giả thuyết domain shift có thể đáng kiểm tra; không thể kết luận rằng attention đã nhìn đúng `like` nhưng chính điều đó gây ra lỗi. Cũng không thể quy lỗi cho việc model “không chú ý tới `like`”.

### 2. Hai mệnh đề mang cảm xúc trái chiều

Với **“I thought this movie would be bad, but it was actually excellent.”**, `bad` nhận attention **0,1588**, nhỉnh hơn `excellent` (**0,1427**); `would` nhận **0,1202** và `actually` **0,0883**. Model dự đoán Negative, nhưng P=**0,6613** cho thấy đầu ra ít áp đảo hơn hai lỗi còn lại.

**Giả thuyết:** model có thể giữ cue tiêu cực ở mệnh đề đầu mạnh hơn phần đảo chiều sau `but`, thay vì kết hợp toàn câu để nhận ra đánh giá cuối cùng là Positive. **Đối chiếu:** `bad` đứng trên `excellent` trong thống kê attention và lớp Negative thắng, phù hợp với giả thuyết này; chênh lệch attention nhỏ, đồng thời cả hai cue đều nhận được attention. Đây là một dấu hiệu để điều tra quan hệ giữa các mệnh đề, không phải bằng chứng rằng attention vào `bad` làm model sai.

### 3. Phủ định và phần đính chính

Với **“The movie was not bad; it was actually quite good.”**, attention nhận được của `bad` là **0,2297**, cao hơn `quite` (**0,1835**), `good` (**0,0981**) và `not` (**0,0808**). Model dự đoán Negative với P=**0,9954**.

**Giả thuyết:** model có thể phản ứng mạnh với từ `bad` nhưng biểu diễn chưa tốt phạm vi phủ định trong `not bad` và phần đính chính `actually quite good`. **Đối chiếu:** phân bố attention và dự đoán Negative có vẻ nhất quán với giả thuyết này. Tuy nhiên, thống kê attention trung bình không đo ảnh hưởng của từng token lên logit; model có thể đang dùng tương tác khác giữa các token hoặc các tham số của bộ phân loại. Muốn kiểm tra giả thuyết cần so sánh có kiểm soát, chẳng hạn thay hoặc bỏ riêng `not`, `bad`, `good` rồi quan sát thay đổi logit.

## Kết luận

Trong ba lỗi được chọn, attention có lúc bám vào cue mà người đọc xem là quan trọng (`like`), có lúc phân bổ gần nhau cho cue trái chiều (`bad` và `excellent`), và có lúc cấp trọng số thấp hơn cho từ phủ định (`not`). Các mẫu này gợi ý những giả thuyết khác nhau, nhưng không chứng minh quan hệ nhân quả giữa attention và lỗi dự đoán. Kết luận chắc chắn từ sáu probe là model dự đoán đúng 3 câu và sai 3 câu đã chọn; chúng không đại diện cho toàn bộ test set và không được dùng để ước lượng accuracy.
