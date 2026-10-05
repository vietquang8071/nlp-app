# Error Analysis: Word Representations and Embeddings


## I. 3 Cặp Similarity Đúng

### 1. `doctor` → `physician` (Word2Vec)
* **Observed:** Trong Experiment 2, `physician` xếp hạng 1 trong Top-5 từ gần `doctor` nhất với cosine similarity đạt **0.7949**. Trong Experiment 1, độ tương đồng giữa hai từ này cũng duy trì ở mức cao (**0.8355 – 0.8940**).
* **Expected:** Hai từ này là từ đồng nghĩa trực tiếp, cùng chỉ nghề nghiệp bác sĩ y khoa, dự kiến phải có độ tương đồng ngữ nghĩa cao nhất (đúng như dự đoán tại **Prediction 1**).
* **Possible explanation:**
  * **Distributional Hypothesis:** Cả hai từ đều đóng vai trò ngữ pháp giống nhau (danh từ chỉ người) và thường xuyên kết hợp với cùng một nhóm vị ngữ/tân ngữ y khoa (`examine`, `treated`, `patient`, `prescribe`, `diagnose`).
  * Thuật toán Skip-gram ánh xạ thành công các vector từ xuất hiện trong ngữ cảnh tương tự về gần nhau trong không gian dense vector.
* **Evidence from corpus:** Trong tập tin trích xuất C4, các cụm từ thể hiện sự tương đương xuất hiện lặp lại:
  * *"consult your doctor or physician"*
  * *"board-certified physician / licensed doctor"*
* **Nguyên nhân chính:** `frequency` vừa đủ, ngữ cảnh xuất hiện đồng nhất.

---

### 2. `football` → `baseball`, `basketball`, `soccer` (Word2Vec)
* **Observed:** Trong Experiment 2, Top-3 từ gần nhất của `football` lần lượt là:
  1. `baseball` (0.8323)
  2. `basketball` (0.8104)
  3. `soccer` (0.7679)
* **Expected:** Các môn thể thao đồng cấp cùng thuộc trường từ vựng thể thao đối kháng có bóng, dự kiến có vector biểu diễn rất gần nhau.
* **Possible explanation:**
  * Các từ này chia sẻ tập ngữ cảnh cực kỳ đặc trưng: xuất hiện chung với các động từ (`play`, `watch`, `coach`), danh từ giải đấu (`game`, `team`, `league`, `championship`, `season`), và tính từ (`high school`, `college`, `professional`).
  * Chiều không gian dense vector đã phân cụm thành công nhóm khái niệm thể thao riêng biệt khỏi các thực thể khác.
* **Evidence from corpus:**
  * *"high school football, basketball, and baseball games"*
  * *"sports news covering football, soccer, and basketball championships"*
* **Nguyên nhân chính:** `context window` bao quát được các cấu trúc liệt kê đồng vị, `domain bias` đồng nhất trong các bài báo thể thao.

---

### 3. `computer` → `desktop`, `device`, `laptop`, `server` (Word2Vec)
* **Observed:** Trong Experiment 2, Top các từ gần `computer` nhất gồm:
  1. `desktop` (0.7840)
  2. `browser` (0.7522)
  3. `device` (0.7431)
  4. `laptop` (0.7316)
  5. `server` (0.6991)
* **Expected:** Các từ liên quan đến thiết bị phần cứng, môi trường tin học và kiến trúc máy tính phải nằm sát nhau trong không gian biểu diễn.
* **Possible explanation:**
  * Mô hình học được quan hệ giữa danh từ bao hàm (`computer`, `device`) và các phân nhánh cụ thể (`laptop`, `desktop`, `server`).
  * Chúng chia sẻ các hành động thao tác: `install`, `connect`, `reboot`, `system`, `screen`, `internet`.
* **Evidence from corpus:**
  * Ngay trong dòng số 2 của C4 mẫu (`Mac OS X Lion` discussion): *"I've got a 500gb internal drive and a 240gb SSD... booting from a different drive... clone to desktop/laptop"*.
* **Nguyên nhân chính:** Ngữ cảnh công nghệ thông tin rõ nét, ít bị phân tán nghĩa.

---

## II. 3 Cặp Similarity Sai / Bất Ngờ

### 1. `car` → `while` (0.9744), `house` (0.9720), `after` (0.9671)
* **Observed:** Trong Experiment 1 (Co-occurrence Matrix với `window = 5`), các từ gần `car` nhất lại là các liên từ / giới từ / trạng từ thông dụng (`while`, `after`) và danh từ chung chung (`house`, `company`, `game`) với score cực cao (> 0.96). Tương tự, `doctor` lại gần `child` (0.9456), `vehicle` (0.9248), `or` (0.9220).
* **Expected:** `car` phải gần các từ mang tính liên kết phương tiện như `vehicle`, `automobile`, `driver`, `road`.
* **Possible explanation:**
  * **Hạn chế nghiêm trọng của Raw Count Co-occurrence:** Mô hình đếm thô không có cơ chế phạt từ xuất hiện quá nhiều. Các function words / stop words như `while`, `after`, `or` xuất hiện với tần suất khổng lồ ở mọi văn bản, khiến hầu hết mọi từ đều co-occur với chúng.
  * Vector của các từ tần suất cao này chiếm độ dài lớn và kéo góc cosine của các danh từ thông thường về cùng một hướng tổng quát.
* **Evidence from corpus:**
  * Hầu như mọi câu mô tả hành động có từ `car` đều có mặt liên từ: *"while driving the car"*, *"after getting out of the car"*.
* **Nguyên nhân chính:** `frequency` quá cao của hư từ, `noisy data`, thiếu chuẩn hóa trọng số.

---

### 2. `hospital` → `indiana` (0.6886), `cincinnati` (0.6782), `yale` (0.6694), `alabama` (0.6691) (Word2Vec)
* **Observed:** Trong Experiment 2, ngoại trừ từ `clinic` (0.7094) ở vị trí số 1, cả 4 vị trí còn lại trong Top-5 của `hospital` đều là tên các địa danh / trường đại học tại Mỹ (`indiana`, `cincinnati`, `yale`, `alabama`), thay vì các thuật ngữ y khoa thông thường như `doctor`, `nurse`, `patient`, `emergency`.
* **Expected:** `hospital` dự kiến gần với các cơ sở y tế (`clinic`, `infirmary`) hoặc các đối tượng y tế chuyên môn (`healthcare`, `medical`, `medicine`).
* **Possible explanation:**
  * **Domain Bias & Named Entity Bias:** Trong tiếng Anh báo chí và web scrape (C4), tên các bệnh viện thường được cấu tạo theo dạng: `[Địa danh / Đại học] + Hospital` (ví dụ: *Indiana University Hospital*, *Cincinnati Children's Hospital*, *Yale New Haven Hospital*, *University of Alabama Hospital*).
  * Trong cửa sổ context window (`window = 5`), danh từ riêng đứng liền kề `hospital` lặp đi lặp lại rất nhiều lần, khiến mô hình Skip-gram coi các địa danh này có quan hệ ngữ nghĩa tương tự hoặc dự đoán lẫn nhau rất mạnh.
* **Evidence from corpus:**
  * Minh chứng rõ rệt ngay trong kết quả tìm kiếm Semantic Search (Rank 4 query `medical treatment`):
    > *"the **indiana hospital** heart institute has one of the largest most experienced cardiac surgery team in south india... performed at **indiana hospital**..."*
* **Nguyên nhân chính:** `domain bias`, `named entity co-occurrence patterns`, `corpus nhỏ` chưa đủ đa dạng để làm loãng tên riêng địa phương.

---

### 3. `doctor` → `spouse` (0.7228), `novak` (0.6359), `husband` (0.6327) (Word2Vec)
* **Observed:** Trong Experiment 2, từ `doctor` ngoài `physician` (0.7949) và `child` (0.7066) thì xuất hiện các từ chỉ quan hệ gia đình (`spouse`, `husband`) và một tên riêng lạ (`novak`) với similarity khá cao.
* **Expected:** Top-5 của `doctor` nên là các nhân sự y tế khác (`nurse`, `surgeon`, `specialist`, `practitioner`) hoặc chuyên ngành (`medicine`, `clinic`).
* **Possible explanation:**
  * **Corpus nhỏ & Mất cân bằng nội dung :** Mẫu 10,000 bài viết C4 ngẫu nhiên có chứa các bài viết về tiểu sử, phỏng vấn nhân vật, tin tức đời tư của bác sĩ hoặc hướng dẫn bảo hiểm/thừa kế nhắc đến *"doctor and spouse / husband"*.
  * Tên riêng `novak`: Nhiều khả năng có một nhân vật cụ thể có tên Novak được nhắc tới nhiều lần kèm danh xưng bác sĩ trong tập 10,000 bài viết (ví dụ: *"Dr. Novak said..."*), khiến vector của `novak` bám chặt lấy `doctor`.
* **Evidence from corpus:**
  * Văn bản tiểu sử bác sĩ hoặc bài viết pháp lý/bảo hiểm gia đình: *"coverage for the doctor, spouse, and dependent children"*.
* **Nguyên nhân chính:** `corpus nhỏ` (dẫn tới hiện tượng spurious correlation), `insufficient training data` để học được toàn bộ trường từ vựng mở rộng của ngành y tế.

---

## III. Phân tích hiện tượng đặc biệt từ thực nghiệm đối chiếu Prediction

### 1. Hiện tượng suy giảm tương đồng khi tăng Embedding Dimension (Experiment 4)
* **Quan sát:** Ở Dimension = 50, `Sim(doctor, physician) = 0.7983`. Khi nâng lên Dimension = 300, điểm này tụt dốc xuống **0.5575** (giảm hơn 24%).
* **Nguyên nhân:**
  * Hoàn toàn khớp với nhận định tại **Prediction 3**: *"Tăng số chiều không bảo đảm chất lượng tăng... với corpus nhỏ, số chiều lớn có thể học nhiễu"*.
  * Cỡ dữ liệu 10,000 tài liệu (~ vài triệu từ) là quá nhỏ so với không gian 300 chiều. Mô hình bị phân tán tham số, các chiều vector học phải nhiễu ngẫu nhiên dẫn đến khoảng cách giữa các từ đồng nghĩa bị kéo giãn ra.

### 2. Hiện tượng thay đổi similarity khi tăng Context Window (Experiment 3)
* **Quan sát:**
  * `doctor - hospital` tăng liên tục từ **0.4390** (Window 2) $\rightarrow$ **0.4876** (Window 5) $\rightarrow$ **0.5377** (Window 10).
  * Trong khi đó `doctor - physician` đạt cao nhất ở Window 2 (**0.7542**).
* **Nguyên nhân:**
  * Khớp với **Prediction 2**: Context window nhỏ (k=2) nắm bắt quan hệ **cú pháp / chức năng thay thế trực tiếp** (doctor và physician thay thế được cho nhau trong câu).
  * Context window lớn (k=10) nắm bắt quan hệ **chủ đề / ngữ cảnh rộng** (hospital và doctor xuất hiện cùng một đoạn văn về y tế nhưng ít khi đứng kề sát nhau).
