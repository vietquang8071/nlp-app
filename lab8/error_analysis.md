# Error Analysis — Sentiment Classification

## Phạm vi và cách đọc

Phân tích này dùng kết quả **Experiment 5 — Domain Shift** trong `experiments.ipynb`. Mô hình là `distilbert-base-uncased`, fine-tune trên IMDb; notebook đánh giá trên IMDb (in-domain) và Yelp (out-of-domain), với đầu vào bị cắt ở 128 token. Sáu ví dụ dưới đây được chọn từ các review lỗi đã lưu trong `results/experiment5/ex5_imdb_error_samples.csv` và `results/experiment5/ex5_yelp_error_samples.csv`.

Notebook không lưu confidence theo từng review. Vì vậy, confidence trong bảng được tính lại bằng softmax từ checkpoint `results/experiment2/finetuned_transformer_best.pt`, cùng tokenizer và giới hạn 128 token. Đây là xác suất của nhãn mà mô hình đã dự đoán. Ngưỡng **90%** được dùng trong báo cáo để đánh dấu ví dụ “rất tự tin”; xác suất softmax cao không đồng nghĩa với xác suất đã được hiệu chỉnh tốt.

- **False Positive (FP):** nhãn thật Negative nhưng mô hình dự đoán Positive.
- **False Negative (FN):** nhãn thật Positive nhưng mô hình dự đoán Negative.

| Text | True | Pred | Confidence | Error type | Hypothesis |
|---|---|---|---:|---|---|
| **FP1 — IMDb:** “I too found myself in tears … a film of such awe-inspiring awfulness … it fails miserably.” | Negative | Positive | 92.10% (Positive) | False Positive — rất tự tin | **[sarcasm; context]** “In tears” và “awe-inspiring” có vẻ tích cực nếu đọc riêng, nhưng “awfulness” và “fails miserably” làm rõ giọng mỉa mai: câu “in tears” nằm trong lời chê châm biếm, không phải lời khen cảm động. Mô hình có thể đã bám vào các từ mang sắc thái tích cực mà không kết hợp chúng với ngữ cảnh phủ định. |
| **FP2 — IMDb:** “The original is a masterpiece … unfortunately my fears were realized. This is a humorless piece … unmemorable piece of fluff.” | Negative | Positive | 92.09% (Positive) | False Positive — rất tự tin | **[context]** Lời khen “masterpiece” nói về bản phim gốc, còn nhãn cảm xúc áp dụng cho bản làm lại đang bị chê. Mô hình có thể đã gán nhầm cảm xúc giữa hai đối tượng được so sánh thay vì theo dõi phim nào là đối tượng chính của review. |
| **FP3 — Yelp:** “Went in fully intending to join … no Bullsh*t high pressure sales … I was so wrong!!! beware of this place.” | Negative | Positive | 92.08% (Positive) | False Positive — rất tự tin | **[negation; tokenization; domain-specific expression]** Kết luận “I was so wrong” đảo ngược kỳ vọng ban đầu; “no Bullsh*t” và “beware” cũng báo hiệu đánh giá xấu. Yelp dùng văn phong khẩu ngữ, dấu câu dồn dập và cách viết né kiểm duyệt “Bullsh*t”; mô hình có thể không kết hợp tốt các dấu hiệu này, nhất là khi chuyển từ review phim sang review dịch vụ. |
| **FN1 — IMDb:** “I had a heck of a good time … undeniably cheaply-made … scripting … very good … dialogue is fantastic … a thinking film … a sleazy story.” | Positive | Negative | 93.68% (Negative) | False Negative — rất tự tin | **[ambiguous sentiment; context; label ambiguity]** Review vừa chê chất lượng sản xuất, diễn xuất và cốt truyện, vừa khen kịch bản, lời thoại và trải nghiệm xem; người viết còn nói rõ họ đã có khoảng thời gian vui vẻ. Mô hình có thể đã cộng dồn các tính từ tiêu cực ở cấp độ từng khía cạnh và bỏ qua đánh giá tổng thể tích cực. Đây là trường hợp cảm xúc hỗn hợp nên nhãn tổng thể khó suy ra chỉ từ một vài từ. |
| **FN2 — Yelp:** “What more can you want? … The Mirage will be my ‘go to’ from now on … Great experience all together … the Mirage wins the all-around favorite.” | Positive | Negative | 92.67% (Negative) | False Negative — rất tự tin | **[long-range dependency; context]** Review dài 292 token, nhưng đầu vào bị cắt ở 128 token. Kết luận tường minh “Great experience all together” và “wins the all-around favorite” nằm sau phần bị cắt nên mô hình không nhận được chúng. Những đoạn còn lại vẫn có lời khen, nhưng phần kết bị mất có thể làm tín hiệu tổng thể yếu đi. |
| **FN3 — IMDb:** “First time … I liked it a lot … inventive and funny from start to finish … Great stuff, reaffirming my love of silent film comedy.” | Positive | Negative | 82.39% (Negative) | False Negative | **[domain-specific expression; context]** Cụm “rocky viewing” và “survived much worse” mô tả tình trạng bản phim bị hư hại, không phải kết luận rằng phim dở. Các từ chuyên biệt về phim câm và cách kể qua nhiều thời kỳ có thể khiến mô hình gán nhầm lời chê ở một khía cạnh kỹ thuật cho cảm xúc chung về bộ phim, dù phần kết thể hiện sự yêu thích rõ ràng. |

## Hai ví dụ dự đoán sai với độ tự tin cao

Theo ngưỡng 90% đã nêu, **FP1** bị dự đoán Positive với confidence 92.10% dù review mỉa mai bộ phim là tệ; **FN1** bị dự đoán Negative với confidence 93.68% dù người viết nói đã có khoảng thời gian xem vui vẻ và khen kịch bản, lời thoại. FP2, FP3 và FN2 trong bảng cũng vượt ngưỡng 90%. Các trường hợp này cho thấy confidence cao của mô hình chưa phản ánh đáng tin cậy khả năng dự đoán đúng.

## Đối chiếu với kết quả tổng thể

| Tập đánh giá | Vai trò | Số mẫu | Accuracy | Macro-F1 | Lỗi | False Positive | False Negative |
|---|---|---:|---:|---:|---:|---:|---:|
| IMDb | In-domain | 2,497 | 0.7645 | 0.7611 | 588 (23.55%) | 432 | 156 |
| Yelp | Out-of-domain | 5,000 | 0.7612 | 0.7600 | 1,194 (23.88%) | 775 | 419 |

Trên IMDb, recall của lớp Negative là 0.6511, thấp hơn recall lớp Positive 0.8761; mô hình bỏ sót nhiều review tiêu cực và nhầm chúng thành tích cực. Trên Yelp, recall Negative là 0.6900 và recall Positive là 0.8324. Macro-F1 hai miền khá gần nhau, nhưng các ví dụ cụ thể cho thấy mô hình vẫn dễ nhầm mỉa mai, cảm xúc pha trộn, đối tượng được so sánh và tín hiệu tổng thể bị đẩy ra ngoài giới hạn token.

Các giả thuyết trong bảng là cách giải thích dựa trên nội dung review và hành vi mô hình, không phải nguyên nhân đã được kiểm chứng riêng. Đặc biệt, FP/FN trên Yelp có thể chịu ảnh hưởng của domain shift vì mô hình được fine-tune trên IMDb.
