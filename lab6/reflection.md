Qua các thí nghiệm trong [experiments.ipynb](experiments.ipynb), đối chiếu với [predictions.md](predictions.md), [results.md](results.md), [error_analysis.md](error_analysis.md) và các hình trực quan hóa, tôi nhận thấy attention giúp mô hình lựa chọn và kết hợp thông tin theo nội dung đầu vào. Cơ chế này có lợi thế về khả năng kết nối các token và tính toán song song, nhưng chất lượng dự đoán còn phụ thuộc vào representation, thông tin vị trí, dữ liệu huấn luyện và cách tổng hợp đầu ra. Những kết quả dưới đây cho thấy cả lợi ích lẫn giới hạn đó.

Phần cài đặt scaled dot-product attention giúp tôi hiểu rõ ba bước: tính độ tương thích giữa Query và Key, dùng softmax tạo trọng số, rồi lấy tổng có trọng số của các Value. Với cùng một query và cùng điều kiện mask, score lớn hơn sẽ nhận attention weight lớn hơn. Phép trừ giá trị lớn nhất trước khi tính softmax giữ nguyên kết quả về mặt toán học và giảm nguy cơ overflow. Hệ số chia cho căn bậc hai của số chiều Key giúp kiểm soát độ lớn của score khi số chiều tăng. Đây là các chi tiết tính toán cần thiết để triển khai attention ổn định.

Trong **Experiment 1**, câu “The movie was surprisingly good despite a very slow beginning.” nhận phân bố attention không đồng đều. Token `slow` có score lớn nhất, khoảng **4,9766**, và nhận attention **0,425215**, trong khi `good` chỉ nhận **0,004946**. Kết quả phù hợp với dự đoán về quan hệ giữa score và softmax trong `predictions.md`. Tuy nhiên, embedding, phép chiếu Key và Query ở thí nghiệm này đều được khởi tạo ngẫu nhiên. Vì vậy, việc `slow` nhận attention cao chỉ minh họa cơ chế tính trọng số; nó chưa cho thấy mô hình đã học được sắc thái cảm xúc của câu.

**Experiment 2** giữ nguyên Key và thay Query. Phân bố attention thay đổi rõ rệt:

| Token | Attention với Query ban đầu | Attention với Query mới |
|---|---:|---:|
| `slow` | 0,425215 | 0,006418 |
| `movie` | 0,187698 | 0,553964 |
| `good` | 0,004946 | 0,049878 |

Điều này cho thấy attention là một phép lựa chọn thông tin phụ thuộc vào query. Một token có thể nhận trọng số cao trong một phép truy vấn và thấp trong phép truy vấn khác. Đây là ưu điểm khi cần xây dựng nhiều representation theo ngữ cảnh. Đồng thời, nó nhắc tôi rằng attention weight không phải mức độ quan trọng cố định của một từ. Các trường hợp score bằng nhau hoặc có một score vượt trội trong `predictions.md` là những hệ quả lý thuyết của softmax; notebook hiện tại chưa lưu thí nghiệm riêng cho hai trường hợp đó.

Trong **Experiment 3**, BERT được dùng để quan sát attention của hai câu có mệnh đề quan hệ: “The cat that I adopted yesterday is sleeping.” và “The book that I bought yesterday was expensive.” Các hình đang xét layer 0, head 0, trong khi tensor attention có 12 layer và 12 head. Ở câu thứ nhất, query `cat` chú ý nhiều nhất tới `i` (**0,144744**); query `adopted` chú ý nhiều nhất tới `yesterday` (**0,212031**); query `sleeping` chú ý nhiều nhất tới `[SEP]` (**0,160421**), còn `cat` nhận **0,105415**.

Khi đọc câu, tôi kỳ vọng quan hệ giữa `cat` và `sleeping`, hoặc giữa `book` và `expensive`, sẽ nổi bật. Heatmap của một head không thể hiện hoàn toàn kỳ vọng đó. Quan sát này giúp tôi hiểu rằng mỗi head chỉ cung cấp một góc nhìn về quá trình kết hợp thông tin. Chưa thể dựa vào head đang xem để kết luận toàn bộ BERT không học được phụ thuộc giữa các token, nhất là khi thí nghiệm này không có đầu ra tác vụ để đối chiếu. Trực quan hóa hữu ích để hình thành giả thuyết, nhưng cần khảo sát thêm các head, layer và hành vi đầu ra để đánh giá giả thuyết ấy.

**Experiment 4** so sánh LSTM và AttentionClassifier trên IMDb, với 40.000 mẫu train, 5.000 validation và 5.000 test. Hai mô hình dùng embedding 64 chiều, giới hạn đầu vào 100 token và được huấn luyện trong 5 epoch. Kết quả đã lưu là:

| Model | Accuracy | F1 | Thời gian huấn luyện (s) | Số tham số |
|---|---:|---:|---:|---:|
| LSTM | 0,8334 | 0,8328 | 78,53 | 1.313.410 |
| Attention | 0,8362 | 0,8356 | 40,35 | 1.296.770 |

Attention cao hơn LSTM **0,28 điểm phần trăm accuracy** và **0,0028 F1**. Thời gian huấn luyện bằng khoảng **51,4%** thời gian của LSTM, tương ứng nhanh hơn khoảng **1,95 lần** trong lần chạy này. Kết quả phù hợp với lợi thế tính toán song song của self-attention. Tuy nhiên, mức chênh lệch accuracy nhỏ và chưa có kết quả lặp lại qua nhiều seed, nên chưa đủ cơ sở để khẳng định attention luôn chính xác hơn hoặc luôn nhanh hơn LSTM trên mọi cấu hình.

Sự khác biệt về representation giúp giải thích rõ hơn phép so sánh này. LSTM đọc chuỗi theo thứ tự và dùng hidden state cuối `h_n[-1]` làm vector câu. AttentionClassifier tạo vector ngữ cảnh cho từng token bằng self-attention 4 head, sau đó lấy trung bình các vị trí không phải padding. Cả hai cuối cùng đều tạo vector câu 64 chiều, nhưng attention cho phép các token trao đổi thông tin trực tiếp trước bước tổng hợp. Khả năng này có ích về mặt kiến trúc đối với các quan hệ giữa token cách xa nhau; các kết quả hiện có chưa chứng minh mô hình đã xử lý tốt mọi phụ thuộc dài.

Một hạn chế cụ thể của AttentionClassifier trong notebook là **chưa có positional encoding hoặc positional embedding**. Với self-attention không có thông tin vị trí và bước mean pooling hiện tại, việc hoán vị cùng các token hợp lệ trong đầu vào sẽ giữ nguyên vector câu về mặt toán học. Nhận xét này áp dụng khi tập token được giữ lại sau truncation không thay đổi và bỏ qua sai số số học. Mô hình vẫn kết hợp nội dung giữa các từ, nhưng thiếu khả năng phân biệt các câu chỉ khác thứ tự từ. Đây là hạn chế của cấu hình classifier đang dùng; BERT ở Experiment 3 có position embedding. Vì thế, khi đánh giá attention, cần xét cả cách đưa thông tin vị trí vào mô hình.

**Experiment 5** cho thấy chi phí của dense self-attention tăng nhanh khi chuỗi dài hơn. Với `float32`, kích thước một ma trận attention và thời gian benchmark đã lưu như sau:

| Độ dài chuỗi | Số phần tử ma trận | Bộ nhớ cho một ma trận (MiB) | Thời gian trung bình (ms) |
|---:|---:|---:|---:|
| 10 | 100 | 0,000381 | 0,088305 |
| 100 | 10.000 | 0,038147 | 0,304735 |
| 500 | 250.000 | 0,953674 | 11,133753 |
| 1.000 | 1.000.000 | 3,814697 | 23,209649 |
| 10.000 | 100.000.000 | 381,469727 | 2.067,045166 |

Khi độ dài tăng từ 10 lên 1.000 token, số phần tử ma trận tăng **10.000 lần**, đúng với dự đoán về bậc hai trong `predictions.md`. Ở 10.000 token, riêng một ma trận đã cần khoảng **381,47 MiB**. Bộ nhớ thực tế còn bao gồm các tensor khác và có thể tăng thêm theo batch size, số head và các giá trị cần lưu khi huấn luyện. Vì vậy, khả năng tính song song tốt vẫn đi cùng chi phí đáng kể đối với chuỗi dài.

Benchmark này dùng NumPy, đo phần tính `QKᵀ` có scaling và softmax, lấy trung bình 5 lần sau warm-up. Nó chưa bao gồm phép nhân với Value, backward hay toàn bộ mô hình Transformer. Các con số bộ nhớ được tính từ kích thước ma trận, không phải phép đo peak memory. Thời gian thực tế cũng không tăng đúng theo tỷ lệ số phần tử vì còn chịu ảnh hưởng của kích thước phép toán, thư viện tính toán và phần cứng. Những giới hạn này cần được giữ lại khi diễn giải đồ thị runtime.

Phần **Application — Context-aware sentiment** cho thấy điểm số tổng thể tốt vẫn có thể đi kèm lỗi ở câu đơn giản. Cả ba câu minh họa trong notebook đều được dự đoán là Negative. Với “I like this movie.”, dự đoán sai và xác suất softmax của lớp Negative là **0,9891**; với “I do not like this movie.”, dự đoán đúng và xác suất lớp Negative là **0,9991**; với câu có phần kết “but it was actually excellent”, dự đoán sai và xác suất lớp Negative là **0,6613**. Hai câu đầu tạo thành một cặp đối chiếu hữu ích: thêm phủ định làm xác suất thay đổi, nhưng lớp dự đoán không đổi. Do đó, dự đoán đúng riêng câu có `not` chưa đủ để chứng minh mô hình xử lý tốt quan hệ phủ định.

Heatmap sentiment hiện có cũng cho thấy mô hình vẫn cấp attention cho thông tin tích cực. Trong câu “I thought this movie would be bad, but it was actually excellent.”, query `excellent` chú ý tới chính nó khoảng **0,61**, còn query `would` chú ý tới `bad` khoảng **0,52**. Theo thống kê trung bình trong `error_analysis.md`, `bad` nhận **0,1588** và `excellent` nhận **0,1427**. Giả thuyết rằng mô hình xử lý chưa tốt quan hệ tương phản giữa hai mệnh đề phù hợp với dự đoán Negative, nhưng các quan sát này chưa xác định nguyên nhân gây lỗi. Đầu ra còn phụ thuộc vào Value, các phép chiếu, pooling và classifier; trung bình qua các head cũng có thể che mất khác biệt giữa chúng.

Một đối chứng khác trong `error_analysis.md` là câu “I like this movie.”: `like` nhận attention trung bình cao nhất, nhưng dự đoán vẫn sai. Trường hợp “The movie was not bad; it was actually quite good.” lại gợi ý khó khăn với phạm vi phủ định khi `bad` nhận trọng số cao hơn `not` và `good`. Những trường hợp này củng cố cách sử dụng attention như nguồn bằng chứng hỗ trợ phân tích. Việc gán lỗi cho domain shift, phủ định hay quan hệ giữa các mệnh đề cần được xem là giả thuyết và kiểm tra bằng hành vi mô hình. Sáu probe được chọn trong báo cáo lỗi có nhãn thủ công và được chọn theo kết quả đúng/sai, nên tỷ lệ 3 đúng, 3 sai không phải ước lượng accuracy trên dữ liệu mới.

Các ưu điểm và hạn chế mà tôi rút ra từ bài thực hành có thể đối chiếu như sau:

| Khía cạnh | Ưu điểm của attention | Hạn chế cần xét |
|---|---|---|
| Lựa chọn thông tin | Trọng số thay đổi theo query, tạo cách kết hợp thông tin linh hoạt. | Trọng số lớn chỉ phản ánh phép tính attention đang xét; chưa bảo đảm token đó quyết định lớp dự đoán. |
| Tương tác giữa token | Cho phép kết nối trực tiếp các vị trí trong chuỗi được đưa vào mô hình. | Cần thông tin vị trí và representation phù hợp để phân biệt thứ tự, phạm vi phủ định và quan hệ giữa mệnh đề. |
| Hiệu quả tính toán | Có thể xử lý các vị trí song song; lần chạy IMDb này cho thời gian huấn luyện thấp hơn LSTM. | Dense attention tạo tương tác theo bậc hai của độ dài chuỗi; tốc độ đo được phụ thuộc cấu hình và phần cứng. |
| Phân tích mô hình | Heatmap và trọng số giúp tìm các quan hệ đáng kiểm tra. | Một head hoặc attention trung bình chưa giải thích đầy đủ output và không chứng minh quan hệ nhân quả. |
| Chất lượng dự đoán | Classifier đạt accuracy 83,62% trên test split IMDb đã lưu. | Vẫn có lỗi với câu ngắn, phủ định và cảm xúc trái chiều; xác suất softmax cao không bảo đảm dự đoán đúng. |

Để phát triển bài thực hành, tôi sẽ ưu tiên bổ sung thông tin vị trí và đối chiếu với cấu hình hiện tại trên cùng cách chia dữ liệu. Sau đó, cần lặp lại huấn luyện qua nhiều seed, dùng validation để chọn cấu hình và giữ test cho đánh giá cuối. Các cặp câu thay đổi có kiểm soát ở `not`, từ chỉ cảm xúc hoặc thứ tự mệnh đề sẽ giúp kiểm tra giả thuyết từ attention. Với những câu dài hoặc có từ hiếm, cần ghi nhận tỷ lệ token bị cắt và token chuyển thành `<UNK>`. Giới hạn 100 token có thể bỏ phần cuối review dài; các câu chẩn đoán đã xét đều nằm dưới giới hạn này nên không có căn cứ quy lỗi của chúng cho truncation. Tác động của vocab 20.000 từ và token `<UNK>` cần được kiểm tra riêng. Việc lưu checkpoint, vocab, dự đoán và attention từng head cũng giúp các nhận xét có thể được kiểm tra lại sau khi đóng kernel.

*Ghi chú về phiên bản kết quả: notebook hiện tại đã chạy được cell trực quan hóa cuối và lưu heatmap cho câu kết thúc bằng “actually excellent”. Ghi chú về `SyntaxError` trong `error_analysis.md` phản ánh trạng thái trước đó. Phần reflection này dựa trên nội dung và kết quả đang được lưu trong thư mục.*
