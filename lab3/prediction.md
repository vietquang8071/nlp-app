# Prediction trước Experiment

## Prediction 1 — Những từ nào gần nhau nhất?

**Prediction:** `doctor` và `physician` sẽ gần nhau nhất. `hospital` có thể tương đối gần với hai từ này; `car` và `banana` dự kiến ít liên quan hơn với nhóm từ y tế.

**Reason:** `doctor` và `physician` gần như đồng nghĩa, thường xuất hiện trong các ngữ cảnh tương tự. `hospital` có quan hệ ngữ nghĩa với lĩnh vực y tế nhưng không đồng nghĩa trực tiếp. `car` và `banana` thuộc các nhóm nghĩa khác. Tuy nhiên, kết quả thực tế phụ thuộc vào corpus, cách tạo biểu diễn và cách tính similarity.

**Confidence:** Cao.

## Prediction 2 — Tăng context window từ 2 lên 5 có làm thay đổi similarity không?

**Prediction:** Có thể có thay đổi; similarity không nhất thiết tăng hoặc giảm đồng đều cho mọi cặp từ.

**Reason:** Context window lớn hơn đưa thêm các từ ở xa hơn vào ngữ cảnh. Điều này có thể giúp biểu diễn phản ánh chủ đề rộng hơn, nhưng cũng có thể thêm nhiễu hoặc làm mờ các quan hệ ngữ pháp/ngữ nghĩa cục bộ. Vì vậy, một số cặp từ có thể trở nên gần nhau hơn, trong khi các cặp khác xa nhau hơn. Kết quả còn phụ thuộc vào corpus và phương pháp biểu diễn.

**Confidence:** Cao.

## Prediction 3 — Tăng embedding dimension từ 50 lên 100 rồi 300 có chắc chắn cải thiện chất lượng không?

**Prediction:** Không. Tăng số chiều không bảo đảm chất lượng tăng.

**Reason:** Nhiều chiều hơn có thể giúp mô hình biểu diễn được nhiều đặc trưng hơn, nhưng cũng cần đủ dữ liệu và cách huấn luyện phù hợp. Với corpus nhỏ, số chiều lớn có thể học nhiễu, khái quát hóa kém hoặc tốn thêm bộ nhớ và tính toán. Chất lượng cần được đánh giá trên mục tiêu cụ thể, chẳng hạn word similarity hoặc hiệu quả của tác vụ downstream.

**Confidence:** Cao.

## Prediction 4 — `doctor` và `physician` có chắc chắn gần nhau nếu corpus chỉ có 100 câu không?

**Prediction:** Không chắc chắn. Chúng có thể gần nhau, nhưng biểu diễn học từ corpus nhỏ có thể không phản ánh được quan hệ đó đáng tin cậy.

**Reason:** Với 100 câu, hai từ có thể xuất hiện quá ít lần hoặc không xuất hiện trong các ngữ cảnh tương tự. Khi dữ liệu thưa, co-occurrence statistics và embedding dễ bị thiếu ổn định. Kết quả còn phụ thuộc vào nội dung corpus, tần suất từ, thuật toán và cách huấn luyện. Nếu corpus phù hợp và có đủ ví dụ liên quan thì chúng vẫn có thể được biểu diễn gần nhau.

**Confidence:** Trung bình.

---
